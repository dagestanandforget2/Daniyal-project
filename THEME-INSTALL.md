# Installing the Athari theme on Shopify (without touching your live theme)

The `theme/` folder is a complete Shopify Online Store 2.0 theme. `athari-theme.zip` is the same folder, zipped and ready to upload.

Uploading adds it to your theme library as an **unpublished** theme. Your current live theme is not changed, replaced or unpublished by any step below. Do not click **Publish** until you have previewed it and want to switch.

## Steps

1. In Shopify admin, open **Online Store → Themes**.
2. Scroll to **Theme library**, click **Add theme → Upload zip file**, and choose `athari-theme.zip`.
3. Wait for it to finish. It appears under "Theme library" as **Athari**. It is not live.
4. Click **Customize** on Athari to edit text, the shelf collection and the menus, or **… → Preview** to browse your real store with the new design. Previews use your real products, cart and checkout.
5. Check: home page, a collection, a product with sizes (thobes), add to cart, the cart page, search, and the policy pages.
6. When you are happy, **Publish** from the theme's menu. Your old theme moves back to the library, so you can switch back at any time.

## Settings to review

- **Theme settings → Brand:** accent colour, the Arabic wordmark (`دار الأثري`, change it if your spelling differs), and a top bar message.
- **Header and footer menus:** the theme reads your existing `main-menu` and `footer` menus.
- **Home page → Hero with 3D shelf:** headline, intro text and which collection feeds the shelf (defaults to All Books; only in-stock products appear).
- **Home page → Product list:** which collection to list and how many products.
- **Home page → Collection list:** add Collection blocks to choose and order them. With none, it lists your collections automatically and hides the "Auto:" ones.

## Not included (check before publishing)

- Customer account pages use Shopify's new customer accounts. If you use the classic account pages, tell me and I will add them.
- Gift card and password-page templates are not included.
- Apps that inject into theme code (reviews, popups, etc.) usually need to be re-enabled for a new theme in their own settings. Check each one.
- Fonts come from Google Fonts and the 3D shelf loads Three.js from cdnjs.
