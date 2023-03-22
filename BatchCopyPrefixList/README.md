# CopyPrefixListAcrossRegion

## 简介

批量建立或者拷贝prefixlist方法，可以支持同区域或者跨区域，支持prefixList过滤

#### 模拟执行:

```
python3 CopyPrefixListAcrossRegion.py --RegionFrom=us-east-1 --RegionTo=us-east-2 --PrefixListIds="pl-00dd4bd2c3a3d15b0,pl-05786af78fddce7f1"
```

#### 参数： 

* RegionFrom: 源区域，比如us-east-1
* RegionTo: 目标区域，比如us-east-2
* PrefixListIds： 过滤prefixList id, 逗号分隔

#### 执行结果:

会在目标区域按照条件建立非过托管的 prefixList

# CreatePrefixList

## 简介

批量建立或者拷贝prefixlist方法，基于从console导出的csv文件

#### 模拟执行:

```
python3 CreatePrefixList.py --region=us-east-1 --path='/Users/benxiwan/Downloads/us-east-2/'  --max_entries=50

```
#### 参数： 

* region: 目标区域，比如us-east-2
* path: 本地csv文件的路径
* max_entries 最大的entry数