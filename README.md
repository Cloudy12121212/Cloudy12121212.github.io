# Cloudy’s Corner

纯静态个人主页，部署至 GitHub Pages。无 Python 后端、数据库、留言板、简历申请或管理员入口。左右分页、Liquid Glass 视觉、中英文切换、项目筛选与详情弹窗、动态照片墙及生活模块保留。

## 更新资料

编辑 `public/data/en.json` 和 `public/data/zh.json`。分别包含公开个人资料、学校、实习、项目、生活内容及界面翻译。所有进入这些文件的资料都会公开。

## 添加摄影图片

将原图放入本机 `public/photos/`。支持 JPG、JPEG、PNG、WebP、AVIF；BMP 需先转换。可在该目录 `photos.json` 中补充照片描述。原图不上传 GitHub，构建脚本以最长边 2400 像素生成 JPEG 副本。只上传 `site/photos/` 的压缩版本。

## 构建与预览

macOS 自带 Python 3 与 sips 即可，无第三方依赖。

```sh
python3 scripts/build_static.py
python3 -m http.server 8000 --directory site
```

访问 http://localhost:8000 。不要直接双击 HTML，浏览器需通过 HTTP 读取 JSON 和模块脚本。

## 发布

将仓库的 Settings → Pages → Source 设置为 GitHub Actions。仓库每次向 main 推送，`.github/workflows/pages.yml` 会发布 `site/`。每次修改资料、样式或照片后，先重新构建，再提交公开源码和 site 构建结果。GitHub Actions 不执行 macOS 图片压缩，因此 site 构建结果必须提交。

私有简历、管理员令牌、本地数据库、原始照片不进入仓库。旧后端仅在本机 `tmp/legacy-fullstack/` 保留，不参与运行或发布。Cloudflare 不再作为网站依赖，之前创建的空 D1 数据库没有被部署使用。
