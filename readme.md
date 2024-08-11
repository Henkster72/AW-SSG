# Allround Website Static Site Generator (AW-SSG)

Allround Website Static Site Generator (AW-SSG) is a powerful and minimalistic tool designed to create ultra-fast, static HTML websites using Tailwind CSS (for nice formatting) and Jinja2 (with the help of Python) templating. This static site generator is ideal for deployment on Nginx or Apache servers (which most managed hosting providers like one.com uses), offering efficient preprocessing and flexible configuration through environment variables.
It has baked in support for Tailwind, FTP upload, Templating, Syncing (timestamp comparison), Forms (via PHP mailing provided that the hosting provider supports php), "Wiki like" referencing with preprocessor shortcuts and much more!

**Version 0.1**

**Demo Site**: Check out a live demo of a site generated with AW-SSG at [allroundwebsite.com](https://www.allroundwebsite.com).

## Features

- **Optimized for Speed**: Generates minimal HTML and CSS for the fastest possible page load times.
- **Tailwind CSS Integration**: Automatic purging of unused CSS classes, ensuring the smallest possible CSS files.
- **Smart Preprocessing**: Simplifies your workflow by intelligently resolving file paths and variables in your templates.
- **Jinja2 Templating**: Leverage the power of Jinja2 to create dynamic, reusable components in your static site.
- **Environment Configuration**: Control site settings and sensitive information using a `.env` file.
- **FTP Deployment**: Easily upload your site to any managed hosting provider with FTP access.
- **PHP Integration**: Supports form handling and other dynamic features via PHP and PHP Mailer.

## Table of Contents

- [But why?](#why)
- [Installation](#installation)
- [Usage](#usage)
- [Environment configuration](#environment-configuration)
- [Preprocessor shortcuts](#preprocessor-shortcuts)
- [Tailwind CSS purging](#tailwind-css-purging)
- [FTP deployment](#ftp-deployment)
- [Timestamps handling](#timestamps-handling)
- [Social media integration](#social-media-integration)
- [PHP Mailer Support](#php-mailer-support)
- [Icons support](#icons-support)
- [Contributing](#contributing)
- [License](#license)

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
## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Henkster72/AW-SSG.git
    cd AW-SSG
    ```
    
2. **Install dependencies**:Ensure you have Python 3.8+ installed, then install the required Python packages

    ```bash
    pip install -r requirements.txt
    ```

3. **Install Node.js and Tailwind CSS**:Install Node.js dependencies to enable Tailwind CSS purging

    ```bash
    npm install
    ```

4. **IDE Plugin Support: Install AW-SSG as a Package (Optional)**:To set up AW-SSG as a package in your IDE for improved development support, use the provided "setup.py":
    
   ```bash
    python setup.py
    ```

## Usage

1. **Prepare Your Environment**

   - Create a `.env` file in the root directory to define crucial site settings and other configuration values. Be sure that the remote FTP directory is correct; otherwise, you may encounter errors during deployment.

2. **Understand the Base Template**

   - AW-SSG uses `base.html` as the "mother" or base template. This template serves as the foundation for all other templates, such as `index.html` or `contact.html`. The `base.html` template includes common elements like the header and footer, and other templates extend it to maintain consistency across your site.

3. **Automatic Meta Tags and Sitemap Generation**

   - The generator automatically processes the `{{ meta_tags }}` variable in `base.html`, injecting meta tags defined in the `meta.txt` file located in the root folder. For example:
     
     ```
     name;viewport;width=device-width, initial-scale=1.0
     name;description;{{ meta_description }}
     name;keywords;{{ meta_keywords }}
     ```
     
   - The generator also automatically creates a `sitemap.xml` file, ensuring your site is search-engine friendly.

4. **Generating and Deploying the Site**

   - Run the generator script to build your static site:

     ```bash
     python main.py
     ```

   - The generated site will be placed in the `output/` directory. If you have correctly set up the FTP credentials in your `.env` file, you will be prompted to upload the site to your server automatically. This "automagic" upload simplifies the deployment process, making it compatible with most managed hosting providers.

5. **Blog Support**

   - AW-SSG supports blogs using the `blog.html` and `blog_article.html` templates. To create a blog post, use the prefix `blog_` for your template file, such as `blog_my_first_post.html`. The preprocessor recognizes this prefix, automatically generates the post, and adds a reference to it in `blog.html`:

     ```html
     <div class="bg-white p-6 rounded-lg shadow-md card flex flex-col items-center text-center">
         <a href="../blog/{blog_name}/" class="link flex flex-col items-center">
             <img src="{{ '{{ blog_picture }}' | static(1) }}" class="rounded-md" alt="{blog_title}">
             <h3>{blog_title}</h3>
             <em class="text-sm">Published {template_vars['created_time']}</em>
             <span class="link">Read more <span class="pi pi-rightcaret ml-2"></span></span>
             <span class="pi pi-{watermark_icon} ml-2 text-xl basecol"></span>
         </a>
     </div>
     ```

## Environment Configuration

The `.env` file is crucial for configuring AW-SSG. Below are the variables you can define:

- **TITLE_SITE**: The main title of your site.
- **SUBTITLE_SITE**: Subtitle for your site.
- **BASE_URL**: The base URL of your site (e.g., `https://www.yoursite.com/`).
- **OUTPUT_DIR**: The directory where the generated files will be output (default is `output`).
- **GOOGLETAGID**: Your Google Tag Manager ID for analytics.
- **FTP_ADDRESS**: The FTP server address for deployment.
- **FTP_USER**: The FTP username.
- **FTP_PWD**: The FTP password (required for deployment).
- **REMOTE_DIR**: The remote directory on your server where the site will be uploaded.
- **MAIL_ADDRESS**: The email address used for sending emails (if PHP Mailer is installed).
- **MAIL_PWD**: The password for the email account (required for PHP Mailer).
- **PHYSICAL_ADDRESS**: The physical address of your business or entity.
- **X_HANDLE**: The Twitter/X handle associated with your site.
- **MAPS_SHORTCUT**: Google Maps ID for embedding maps.
- **TEL_NO**: Contact number, used for WhatsApp links.
- **WA_TEXT**: Predefined text for WhatsApp contact links.
- **PHPMAILER_INSTALLED**: Set to `TRUE` if PHP Mailer is installed on your server.
- **COOKIE_TEXT**: A short message about cookie usage.
- **COOKIE_ALERT**: A detailed cookie alert message for users.
- **HEADER_TITLE**: The title for the header within `base.html`.
- **HEADER_DESCRIPTION**: The description for the header within `base.html`.
- **HEADER_KEYWORDS**: Keywords for the header within `base.html`.
- **TITLE_404**: Custom title for the 404 error page.
- **TEXT_404**: Custom text for the 404 error page.
- **LINK_404**: Custom link text for redirecting from the 404 error page.

### Important Notes:

- Variables marked as `|crucial` in your `.env` file are mandatory. The static site generation will halt if these are not properly set.
- Variables with the `|open` flag are available for use as lowercase variables directly in your Jinja2 templates.

## Preprocessor Shortcuts

AW-SSG simplifies your templating process by automatically handling common file paths and references:

- **Image Paths**: `{{ picture.avif }}` resolves to `static/images/picture.avif`.
- **HTML Paths**: `{{ blog.html }}` resolves to the `blog/` directory.
- **CSS/JS Paths**: `{{ style.css }}` resolves to `static/style.css`.

These shortcuts allow you to write cleaner and more intuitive templates without hardcoding paths.

## Tailwind CSS Purging

To ensure your site’s CSS is as lean as possible, AW-SSG includes an option to purge unused Tailwind classes during the build process. This feature can be enabled or disabled at the end of the `main.py` script based on user input. This can be used in the `base.html` template like `<link rel="stylesheet" type="text/css" href="{{ tailwind_min.css }}">` 

After generating the site, you can choose whether or not to purge unused Tailwind CSS classes which is automatically done for you (with `
npx tailwindcss -o static/css/styles.css --minify`)
This command strips out any unused Tailwind classes from `tailwind.css` in the root directory, producing a minified CSS file optimized for production.

## FTP Deployment

AW-SSG supports FTP deployment, allowing you to "automagically" upload your generated site to a remote server. Once the site is generated in the `output/` directory, you can opt to upload it directly to your web server using the built-in FTP upload functionality.

After site generation, you will be prompted to proceed with the FTP upload. The upload process utilizes the FTP credentials and settings defined in your `.env` file:

- **FTP_ADDRESS**
- **FTP_USER**
- **FTP_PWD**
- **REMOTE_DIR**

This automated upload process ensures that your site is always up-to-date with minimal manual intervention, making it a valuable tool for maintaining your static website on managed hosting providers.

## Timestamps Handling

AW-SSG compares timestamps from your local output with those on the remote server, using a European time format. This ensures that only updated files are uploaded, saving time and bandwidth during the FTP deployment process.

## Social Media Integration

The `x_handle` environment variable can be used for social media handles or other custom links. For example, you can add an Instagram handle like this:

```env
INSTAGRAM_HANDLE=test|open     
```
Then, in your `contact.html` or any other template:

```html
{% if instagram_handle %}
    <a href="https://instagram.com/{{ instagram_handle }}" class="bg-pink-500 hover:bg-pink-700 text-white py-4 px-8 rounded-full flex items-center justify-center" target="_blank">
        <span class="pi pi-instagram text-3xl mr-2"></span>Follow {{ instagram_handle }} on Instagram
    </a>
{% endif %}
```
This flexible system allows you to easily integrate any social media handle into your templates.

## PHP Mailer Support

If your server supports PHP and you need to send emails from your website, set `PHPMAILER_INSTALLED=TRUE` in your `.env` file. Use the `install_phpmailer.py` script to install PHP Mailer independently. This will enable full email support for contact forms and other dynamic features on your site.

## Icons Support

AW-SSG supports popular icons through `woff2` formatted icon files. To use these icons, include the `popicons.css` in your `base.html` template. For example:

```html
<span class="pi pi-starsfull text-xl"></span>
```
This automatically loads the `popicon.woff2` file, rendering the "stars" icon for this example on your site. The integration of popular icons enhances the visual appeal of your static website.

## Contributing

We welcome contributions to enhance AW-SSG! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

## Future
I want to integrate markdown as default for editing websites. Feel free to contact me on [allroundwebsite.com](https://www.allroundwebsite.com/contact) for collaboration or features which you find, should be integrated.

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit) file for more details.


