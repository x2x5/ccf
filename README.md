# CCF 评级 2026 版

中国计算机学会推荐国际学术会议和期刊目录（2026年）的静态网页版。

## 功能

- 大类过滤（会议 / 期刊）
- 等级过滤（A类 / B类 / C类）
- 研究方向过滤
- 出版社搜索过滤
- 关键词搜索（简称 / 全称 / 出版社）
- 会议/期刊名超链接直达 DBLP

## 数据来源

https://www.ccf.org.cn/Academic_Evaluation/By_category/

## 构建

数据从 `ccf.md` 解析生成 `data.json`，如需重新生成：

```bash
python parse.py
```

## 部署

将 `index.html` 和 `data.json` 部署到任意静态托管服务（GitHub Pages 等）即可。
