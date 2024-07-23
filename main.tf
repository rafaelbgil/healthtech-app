terraform {
  backend "s3" {
    bucket = "state-terraform-fiap"
    key    = "k8s"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

//Assegura existencia do cluster k8s
resource "aws_eks_cluster" "fiap_cluster_k8s" {
  name     = "fiap-cluster-k8s"
  role_arn = "arn:aws:iam::816796163001:role/eksClusterRole"

  vpc_config {
    subnet_ids = [
      "subnet-07fcff39729d74149", "subnet-009269a90efc9c534", "subnet-07dad2a84eae71fcd", "subnet-0f1b0475d2b0c6e3b",
      "subnet-0501b8d52030a411b"
    ]
  }

}

output "endpoint" {
  value = aws_eks_cluster.fiap_cluster_k8s.endpoint
}


resource "aws_eks_addon" "aws-eks-addon-cni" {
  cluster_name = aws_eks_cluster.fiap_cluster_k8s.name
  addon_name   = "vpc-cni"
}


resource "aws_eks_addon" "aws-eks-addon-coredns" {
  cluster_name = aws_eks_cluster.fiap_cluster_k8s.name
  addon_name   = "coredns"
  depends_on = [aws_eks_node_group.fiap_node_group]
}

resource "aws_eks_addon" "aws-eks-addon-kubeproxy" {
  cluster_name = aws_eks_cluster.fiap_cluster_k8s.name
  addon_name   = "kube-proxy"
}

resource "aws_eks_addon" "aws-eks-addon-pod-identity" {
  addon_name   = "eks-pod-identity-agent"
  cluster_name = aws_eks_cluster.fiap_cluster_k8s.name
}

resource "aws_eks_node_group" "fiap_node_group" {
  cluster_name    = aws_eks_cluster.fiap_cluster_k8s.name
  node_group_name = "fiap_node_group"
  node_role_arn   = "arn:aws:iam::816796163001:role/AmazonEKSNodeRole"
  subnet_ids      = aws_eks_cluster.fiap_cluster_k8s.vpc_config[0].subnet_ids
  instance_types  = ["t3.medium"]
  depends_on      = [
    aws_eks_addon.aws-eks-addon-cni, aws_eks_addon.aws-eks-addon-kubeproxy,
    aws_eks_addon.aws-eks-addon-pod-identity
  ]
  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }
}