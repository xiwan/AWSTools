# aws security group migrate script

## acclaim

- this script will create 'sg-id.sh' under the working directory, and execute it automatically
- make sure u set up the 'aws configure' correctly, it require vpc/sg privileges to run
- support multiple sgs migration per time
- not support overwrite existing sg

## how to run the script

```                      
aws_sg_migrate.py [-h] [--profile=alt_profile] [--shell] [--vpc=vpcid] [-src=source_region] [--dest=dest_region] sg_ids
    -h - help
    --profile (or -p) - use alternate aws cli profile
    --shell (or -s)   - wrap commands in shell syntax to capture id
    --vpc   (or -v)   - specify destination VPC ID for new SG
    --src   (or -sc)  - specify source region for new SG
    --dest  (or -ds)  - specify destination region for new SG
    sg_ids - specify sg id in format 'sg1,sg2'
```

## examples

### one security group
```
python3 aws_sg_migrate.py --vpc=vpc-011b77f2d68a64465 --shell --src=us-west-1 --dest=us-east-1 sg-07b9604d48a462801

```

### one security group with custom profile
```
python3 aws_sg_migrate.py --vpc=vpc-011b77f2d68a64465 --shell --src=us-west-1 --dest=us-east-1 --profile=benxiwan sg-07b9604d48a462801

```

### multiple security groups

```
python3 aws_sg_migrate.py --vpc=vpc-011b77f2d68a64465 --shell --src=us-west-1 --dest=us-east-1 sg-07b9604d48a462801,sg-0cdfc352496a87cda

```