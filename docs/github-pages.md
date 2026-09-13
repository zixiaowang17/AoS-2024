# GitHub Pages

- [Repository](https://github.com/zixiaowang17/AoS-2024)
- [Project website](https://zixiaowang17.github.io/AoS-2024/)
- [Dashboard](https://zixiaowang17.github.io/AoS-2024/experiments/aos-2024/report.html?view=apis)
- [Intermediate research records](https://zixiaowang17.github.io/AoS-2024/intermediates/index.html)

GitHub Pages serves the repository root from `main`. `.nojekyll` keeps Markdown, skill
sources, JSON and HTML unchanged. The report and its entire `report-pages/` directory
must be published together. The previous report snapshot on the personal website remains
available so older links continue to work.

## Blog source

Edit [blog-post.md](blog-post.md), then run:

```sh
python3 scripts/build_blog.py
```

The [rendered draft](blog-post.html) uses the saved personal-site layout and links to
the report in this repository. Its screenshot is `docs/dashboard.png`; its template is
`assets/blog-template.html`. The blog remains labeled as a draft. Publishing this archive
does not add a finished blog post to the personal homepage.

## Updating the site

Run the relevant build script, the report regression suite for renderer changes, and
`python3 scripts/check_release.py`. Review the changes before committing and pushing to
`main`; Pages then republishes the files. Check the deployed report and artifact links
after the Pages build finishes.
