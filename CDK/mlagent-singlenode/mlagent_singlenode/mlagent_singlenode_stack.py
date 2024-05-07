from aws_cdk import (
    # Duration,
    CfnOutput,
    aws_sagemaker as sagemaker,
    CfnParameter,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

git_repo_url = "https://github.com/xiwan/AWS-Mlagents"

class MlagentSinglenodeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 定义参数
        instance_type_param = CfnParameter(
            self, "InstanceTypeParam",
            type="String",
            default="g4dn.xlarge",
            allowed_values=["g4dn.xlarge", "g4dn.2xlarge"],
            description="Select instance type"
        )

        volume_size_param = CfnParameter(
            self, "VolumeSizeParam",
            type="Number",
            default="200",
            allowed_values=["100", "200", "500", "1000"],
            description="EBS Volume Size (GiB)"
        )

        node_type_param = self.node.try_get_context('node')
        print(node_type_param)
        # 获取默认 VPC
        defaultVPC = ec2.Vpc.from_lookup(self, "default", is_default=True)
        # 选择私有子网
        public_subnets = [subnet.subnet_id for subnet in defaultVPC.public_subnets]

        # 创建角色并附加权限
        role = iam.Role(self, "InstanceRole", assumed_by=iam.CompositePrincipal(
            iam.ServicePrincipal("ec2.amazonaws.com"),
            iam.ServicePrincipal("sagemaker.amazonaws.com")
        ))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryFullAccess"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"))

        # 创建安全组并开放端口
        security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=defaultVPC, allow_all_outbound=True)
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5005), "Allow Port 5005")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(6006), "Allow Port 6006")

        if node_type_param == "ec2":
            # 创建 SSH 密钥
            ssh_key = ec2.KeyPair.from_key_pair_name(self, "SSHKey", "test01")
            # 查找 AWS Deep Learning AMI GPU PyTorch 2.0 (Ubuntu 20.04) AMI
            ami = ec2.MachineImage.generic_linux(
                {
                    "us-east-1": "ami-051619310404cab17",  
                    "us-east-2": "ami-07b85d3d0ce8bde4e",
                }
            )
            # 创建启动脚本
            user_data = ec2.UserData.for_linux()
            user_data.add_commands(
                "yum update -y",
                "yum install -y git",
                "cd /home/ec2-user",
                f"git clone {git_repo_url}",
            )
            # 创建 EC2 实例
            instance = ec2.Instance(self, "Instance",
                instance_type=ec2.InstanceType(instance_type_param.value_as_string),  # 或 ec2.InstanceType("G5")
                machine_image=ami,
                vpc=defaultVPC,
                role=role,
                security_group=security_group,
                key_name=ssh_key.key_pair_name,
                block_devices=[
                    ec2.BlockDevice(
                        device_name="/dev/xvda",
                        volume=ec2.BlockDeviceVolume.ebs(
                            volume_type=ec2.EbsDeviceVolumeType.GP3,
                            volume_size=volume_size_param.value_as_number  # 设置 EBS 卷大小为 200 GiB
                        )
                    )
                ],
                user_data=user_data
            )

            # 输出实例 ID
            CfnOutput(self, "InstanceId", value=instance.instance_id)

        if node_type_param == "sagemaker":
            # 创建 SageMaker Notebook 实例
            notebook_instance = sagemaker.CfnNotebookInstance(
                self, "MLAgent-NotebookInstance",
                instance_type=f"ml.{instance_type_param.value_as_string}",
                role_arn=role.role_arn,
                default_code_repository=git_repo_url,
                root_access="Enabled",
                subnet_id=public_subnets[0],  # 选择第一个私有子网
                security_group_ids=[security_group.security_group_id],
                volume_size_in_gb=volume_size_param.value_as_number
            )

            
            # 输出 Notebook 实例地址
            CfnOutput(
                self,
                "NotebookInstanceUrl",
                value=f"https://{self.region}.console.aws.amazon.com/sagemaker/home?region={self.region}#/notebook-instances/openNotebook/{notebook_instance.attr_notebook_instance_name}?view=lab",
                description="Notebook Instance URL"
            )
