# Open Climate Resilience Policies (OCRP)

This repository contains the OCRP website and model policy library, built with [Astro](https://astro.build).

## 🚀 Project Structure

```
/
├── public/              # Static assets (CSS, images)
├── src/
│   ├── content/
│   │   └── policies/    # Policy markdown files
│   ├── layouts/         # Astro layout components
│   └── pages/           # Site pages and routes
├── astro.config.mjs     # Astro configuration
└── package.json
```

## 🧞 Commands

All commands are run from the root of the project:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |

## 📝 Adding New Policies

1. Create a new markdown file in `src/content/policies/`
2. Add the required frontmatter fields (id, title, type, summary)
3. The policy will automatically appear in the policies listing

## 🌐 Deployment

The site automatically deploys to GitHub Pages when you push to the `main` branch.

## 📄 License

Content licensed under CC BY 4.0. © OCRP.
