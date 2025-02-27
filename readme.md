# Allround Website Static Site Generator (AW-SSG)

**AW-SSG** is a minimalistic, wiki-like static site generator that empowers developers to build blazing‐fast, clean, and efficient websites with ease. By combining smart template preprocessing, dynamic base template handling, and environment variable injection, AW-SSG streamlines your workflow—from crafting content to deploying a production-ready site. Modern features like Tailwind CSS integration, FTP deployment, and built-in social media support make it the ideal tool for creating professional online business cards, blogs, or portfolios with minimal fuss.

**Version 0.11**

**Demo Site**: Check out a live demo of a site generated with AW-SSG at [allroundwebsite.com](https://www.allroundwebsite.com).

## Key Features

- **Smart preprocessing & template inheritance**:  
  Automatically processes partials, injects environment variables, and adjusts base templates according to directory depth.

- **Optimized caching & fast builds**:  
  Intelligent timestamp tracking renders only modified pages, ensuring rapid site generation.

- **Modern styling & Tailwind CSS integration**:  
  Leverages Tailwind CSS with automatic purging for lean, production-ready styles.

- **Built-In deployment & social integration**:  
  Seamless FTP upload and CSV-driven social link management streamline your deployment and online presence.

- **Flexible, Wiki-like architecture**:  
  Generate subdirectory overview pages and manage reusable “card” snippets for a modular site structure.

## Table of Contents

- [But why?](#but-why)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Configuration](#environment-configuration)
- [Preprocessor Shortcuts](#preprocessor-shortcuts)
- [Tailwind CSS Purging](#tailwind-css-purging)
- [FTP Deployment](#ftp-deployment)
- [Timestamps Handling](#timestamps-handling)
- [Social Media Integration](#social-media-integration)
- [PHP Mailer Support](#php-mailer-support)
- [Icons Support](#icons-support)
- [Contributing](#contributing)
- [Future](#future)
- [License](#license)

---

## But why?

**The Birth of AW-SSG: My Quest for Simplicity**

As a web developer, I, Henk, was fed up with the bloated, convoluted mess that modern node frameworks had become. Every project felt like it was teetering on the edge, weighed down by unnecessary dependencies and overcomplicated processes. I longed for a return to simplicity, where HTML was clean, CSS was straightforward, and the web was fast.

That’s when Jinja2 caught my eye. Its elegant templating reminded me of the good old days—efficient, flexible, and just what I needed. But while I loved Python frameworks like Flask and FastAPI, their slow serving speeds left much to be desired. I knew I could do better, combining the best of both worlds.

So, I created the Allround Website Static Site Generator (AW-SSG). It’s a minimalistic, ultra-fast tool that leverages Tailwind CSS and Jinja2, served by reliable workhorses like Nginx or Apache. No more wrestling with complex frameworks—just simple, static HTML that’s lightning quick.

And here’s the thing: most small businesses don’t need complex, interactive websites. What they really want is a flexible online business card—a site that looks professional, loads fast, and gets the job done without unnecessary bells and whistles. Static sites are perfect for that, and AW-SSG delivers it beautifully.

With AW-SSG, I added everything I missed: seamless FTP uploads, PHP mailing for forms, and even "wiki-like" referencing. Now, when I deploy a site, I know it’s rock-solid, blazing fast, and exactly how I intended it to be.

If you’re tired of the chaos, and you just want a simple, powerful tool to build that perfect online business card, AW-SSG might just be the simplicity you’ve been looking for.

**But why not use WordPress, Wix, Squarespace, Webflow, or Shopify?**

When people ask me why I didn’t just use WordPress, Wix, Squarespace, Webflow, or Shopify, I get it. These platforms are popular for a reason—they’re convenient, offer drag-and-drop interfaces, and come loaded with features. But here’s the thing: most small businesses don’t need all that complexity.

These platforms often come with a lot of bloat, both in terms of code and features you might never use. They’re designed to be everything to everyone, which often means you’re paying for and managing more than you actually need. Plus, with all the plugins and third-party integrations, you’re introducing potential security vulnerabilities and performance hits.

For a lot of small businesses, what you really need is a fast, reliable, and flexible online business card—something that represents your brand without all the overhead. That’s where the Allround Website Static Site Generator (AW-SSG) comes in. It strips away the unnecessary layers, giving you a lean, ultra-fast website that’s easy to maintain and incredibly secure.

If you’re tired of the chaos, AW-SSG might just be the simplicity you’ve been looking for. Reasons for using AW-SSG:

**Performance and Speed**: Static sites generated by AW-SSG are served as pre-built HTML, CSS, and JavaScript files, which means no server-side processing is required. This leads to significantly faster load times compared to server-side rendered sites, which need to execute code, query databases, and generate content dynamically.

**Security**: Static sites eliminate many common security vulnerabilities associated with server-side applications, such as SQL injection, XSS (Cross-Site Scripting), and server misconfigurations. With no backend to hack, the attack surface is greatly reduced.

**Cost-Effectiveness**: Hosting a static site is often cheaper than hosting a dynamic site because it doesn’t require server-side processing power, databases, or complex infrastructure. Many static sites can be hosted for free or at minimal cost using platforms like GitHub Pages, Netlify, or Vercel.

**Scalability**: Static sites are inherently more scalable than server-side applications because they don’t require server resources to generate pages dynamically. This means you can handle large amounts of traffic with minimal infrastructure, as the same static files are served to every visitor.

**Simplicity**: AW-SSG simplifies the development process by removing the need for backend programming. You don’t have to worry about configuring servers, managing databases, or writing complex server-side logic. This can be especially advantageous for small projects, personal blogs, or portfolio sites where simplicity is key.

**Reduced Maintenance**: Once a static site is generated and deployed, it requires minimal maintenance. There are no servers to manage, no software updates to apply, and no need for constant monitoring of server health. This is in stark contrast to dynamic sites, which require ongoing maintenance and updates.

**Portability**: Static sites are highly portable. They consist of a collection of files that can be easily moved between different environments (local, staging, production) or even between different hosting providers without worrying about compatibility issues with server-side code, databases, or dependencies.

**Environment Agnostic**: Static sites are environment agnostic. They don’t rely on a specific server-side language or framework, making them more future-proof. As long as a web server can serve HTML files, your site will continue to work. This is not the case with server-side applications, which may become obsolete or harder to maintain as languages, frameworks, and technologies evolve.

---

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Henkster72/AW-SSG.git
    cd AW-SSG
    ```

2. **Install Dependencies**:  
   Ensure you have Python 3.8+ installed, then install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install Node.js and Tailwind CSS**:  
   Install Node.js dependencies to enable Tailwind CSS purging:

    ```bash
    npm install
    ```

4. **IDE Plugin Support (Optional)**:  
   To set up AW-SSG as a package in your IDE for improved development support, run:

    ```bash
    python setup.py
    ```

---

## Usage

1. **Prepare Your Environment**  
   Create a `.env` file in the root directory to define crucial site settings and other configuration values. Ensure the remote FTP directory is correctly set to avoid deployment errors.

2. **Understand the Base Template**  
   AW-SSG uses `base.html` as the “mother” template, which provides a foundation for all other templates (e.g., `index.html`, `contact.html`). Templates extend this base to maintain consistency across your site.

3. **Automatic Meta Tags and Sitemap Generation**  
   The generator automatically processes the `{{ meta_tags }}` variable in `base.html`, injecting meta tags defined in the `meta.txt` file, and generates a `sitemap.xml` file for SEO.

4. **Generating and Deploying the Site**  
   Run the generator script to build your static site:

    ```bash
    python main.py
    ```

   The generated site will be placed in the `output/` directory. If FTP credentials are set in your `.env` file, you’ll be prompted to upload the site automatically.

5. **Blog support**  
   AW-SSG supports blogs using the `blog.html` and `blog_article.html` templates. Create a blog post by prefixing your template file with `blog_` (e.g., `blog_my_first_post.html`), and the preprocessor will handle it automatically.

---

## Environment Configuration

Configure AW-SSG via the `.env` file. Key variables include:

- **TITLE_SITE**: Main title of your site.
- **BASE_URL**: Base URL (e.g., `https://www.yoursite.com/`).
- **FTP_ADDRESS, FTP_USER, FTP_PWD, REMOTE_DIR**: For FTP deployment.
- **MAIL_ADDRESS, MAIL_PWD**: For PHP Mailer support.
- *(Additional variables for subtitles, social media, cookie alerts, headers, 404 pages, etc.)*

> **Note**: Variables marked as `|crucial` are mandatory. Variables with the `|open` flag are available in Jinja2 templates as lowercase.

---

## Preprocessor Shortcuts

AW-SSG automates common file path resolutions according to their extensions:

- **Image Paths**: `{{ picture.avif }}` → `static/images/picture.avif` (and so every other image format)
- **HTML Paths**: `{{ blog.html }}` → `blog/index.html`
- **CSS/JS Paths**: `{{ style.css }}` → `static/style.css` (and JS).

---

## Tailwind CSS purging

To ensure your CSS remains lean, AW-SSG includes a Python-powered purging system that:

1. **Extracts Used Classes**:  
   Scans your HTML templates, JavaScript files, and custom CSS (via BeautifulSoup and regex) to collect Tailwind class names.

2. **Generates a Custom Tailwind Config**:  
   Creates a `tailwind.config.js` file with a safelist of extracted classes and custom theme extensions (e.g., animations and keyframes).

3. **Purges and Minifies CSS**:  
   Runs the Tailwind CLI using npx to process your input CSS (e.g., `output/static/style.css`) and outputs a minified file (e.g., `output/static/tailwind_min.css`).

Ensure Node.js is installed and available in your PATH. To install Tailwind CSS with npx:

```
npm install tailwindcss
```

Then, when you run AW-SSG, the purge process executes automatically with:

```
npx tailwindcss -i output/static/style.css -o output/static/tailwind_min.css --config tailwind.config.js --minify
```
This results in a production-ready, minified CSS file that you can reference in your base.html:

<code>\<link rel="stylesheet" type="text/css" href="{{ tailwind_min.css }}"></code>

---

## FTP Deployment

After generation, AW-SSG can automatically upload your site via FTP using credentials specified in your `.env` file (FTP_ADDRESS, FTP_USER, FTP_PWD, REMOTE_DIR).

---

## Timestamps handling

AW-SSG compares local file timestamps (rounded to the minute) with remote ones to upload only updated files—saving time and bandwidth.

---

## Social media integration

Utilize the `x_handle` variable for social links. For example, set:
```env
INSTAGRAM_HANDLE=test|open
```
And in your template:
```html
{% if instagram_handle %}
  <a href="https://instagram.com/{{ instagram_handle }}" class="bg-pink-500 hover:bg-pink-700 text-white py-4 px-8 rounded-full flex items-center justify-center" target="_blank">
    <span class="pi pi-instagram text-3xl mr-2"></span>Follow {{ instagram_handle }} on Instagram
  </a>
{% endif %}
```

---

## PHP Mailer support

Set `PHPMAILER_INSTALLED=TRUE` in your `.env` file and run the `install_phpmailer.py` script to enable email support for forms and other dynamic features.

---

## Icons support

Include custom made `popicons.css` in `base.html` to automatically load popular icons (e.g., via `woff2` files). For example:
```html
<span class="pi pi-starsfull text-xl"></span>
```

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

---

## Future

I plan to integrate Markdown as the default editing format. For collaboration or suggestions, please contact me at [allroundwebsite.com](https://www.allroundwebsite.com/contact).
Also adding support for Github pages and Web3 uploads.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit) file for details.

## Changelog
0.1 Initial commit with basic functionality
0.1.1 Update in subdirectories handling and dilegating processes out of the main.py file. Changed the readme.
