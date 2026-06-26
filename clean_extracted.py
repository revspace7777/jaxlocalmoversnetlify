import os
import re
import shutil

base_dir = r"c:\Users\heath\jaxlocalmovers"

# 1. Delete CallRail assets directory if it exists
callrail_dir = os.path.join(base_dir, "external_assets", "cdn.callrail.com")
if os.path.exists(callrail_dir):
    shutil.rmtree(callrail_dir)
    print(f"Deleted CallRail cdn directory: {callrail_dir}")
else:
    print("CallRail directory does not exist or was already deleted.")

# 2. Get all HTML files
html_files = []
for root, dirs, files in os.walk(base_dir):
    if ".git" in root or ".agents" in root:
        continue
    for file in files:
        if file.lower().endswith(".html"):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to process.")

NEW_TRACKING_SCRIPT = """<script>
document.addEventListener('DOMContentLoaded', function() {
    const paramsToCapture = ['gclid', 'msclkid', 'fbclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    const urlParams = new URLSearchParams(window.location.search);
    
    // Save URL parameters to sessionStorage and localStorage safely
    paramsToCapture.forEach(function(param) {
        if (urlParams.has(param)) {
            const val = urlParams.get(param);
            try {
                sessionStorage.setItem(param, val);
            } catch (e) {
                console.warn('sessionStorage is not accessible:', e);
            }
            try {
                localStorage.setItem(param, val);
            } catch (e) {
                console.warn('localStorage is not accessible:', e);
            }
        }
    });

    // Save landing page and session start time safely
    try {
        if (!sessionStorage.getItem('landing_page') && !localStorage.getItem('landing_page')) {
            sessionStorage.setItem('landing_page', window.location.href);
            localStorage.setItem('landing_page', window.location.href);
        }
        if (!sessionStorage.getItem('session_start_time') && !localStorage.getItem('session_start_time')) {
            sessionStorage.setItem('session_start_time', Date.now());
            localStorage.setItem('session_start_time', Date.now());
        }
    } catch (e) {
        console.warn('Storage is not accessible:', e);
    }

    const populateField = (name, value) => {
        if (value) {
            document.querySelectorAll('input[name="' + name + '"], textarea[name="' + name + '"]').forEach(input => {
                input.value = value;
            });
        }
    };

    // Populate tracking fields directly using their technical parameter names
    paramsToCapture.forEach(function(param) {
        let value = '';
        try {
            value = sessionStorage.getItem(param) || localStorage.getItem(param) || '';
        } catch (e) {}
        populateField(param, value);
    });

    let landingPage = '';
    try {
        landingPage = sessionStorage.getItem('landing_page') || localStorage.getItem('landing_page') || '';
    } catch (e) {}
    
    populateField('landing_page', landingPage);
    populateField('conversion_page', window.location.href);
    populateField('referrer', document.referrer);
    populateField('screen_size', window.screen.width + 'x' + window.screen.height);
    populateField('user_agent', navigator.userAgent);

    document.querySelectorAll('.wpcf7-form, .quote-form').forEach(form => {
        form.addEventListener('submit', function() {
            let startTime = Date.now();
            try {
                startTime = parseInt(sessionStorage.getItem('session_start_time') || localStorage.getItem('session_start_time') || Date.now());
            } catch (e) {}
            const timeOnSiteSeconds = Math.round((Date.now() - startTime) / 1000);
            populateField('time_on_site', timeOnSiteSeconds + ' seconds');
            populateField('submission_timestamp', new Date().toLocaleString());
        });
    });
});
</script>"""

GTAG_INJECTION_HTML = """<!-- Google tag (gtag.js) snippet added by Site Kit -->
<!-- Google Analytics snippet added by Site Kit -->
<!-- Google Ads snippet added by Site Kit -->
<script async="" id="google_gtagjs-js" src="https://www.googletagmanager.com/gtag/js?id=GT-TBBG4KD"></script>
<script id="google_gtagjs-js-after">
window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}
gtag("set","linker",{"domains":["jaxlocalmovers.com"]});
gtag("js", new Date());
gtag("set", "developer_id.dZTNiMT", true);
gtag("config", "GT-TBBG4KD");
gtag("config", "AW-17189356235");
 window._googlesitekit = window._googlesitekit || {}; window._googlesitekit.throttledEvents = []; window._googlesitekit.gtagEvent = (name, data) => { var key = JSON.stringify( { name, data } ); if ( !! window._googlesitekit.throttledEvents[ key ] ) { return; } window._googlesitekit.throttledEvents[ key ] = true; setTimeout( () => { delete window._googlesitekit.throttledEvents[ key ]; }, 5 ); gtag( "event", name, { ...data, event_source: "site-kit" } ); }; 
//# sourceURL=google_gtagjs-js-after
</script>
<script>
  gtag('config', 'AW-17189356235/XOaUCJKfvvAaEMuFw4RA', {
    'phone_conversion_number': '(904) 239-2439'
  });
</script>
"""

# Field name mappings to clean up names with spaces and capitalization
field_replacements = {
    'name="Name"': 'name="name"',
    'name="Email"': 'name="email"',
    'name="Phone"': 'name="phone"',
    'name="Preferred Contact"': 'name="preferred_contact"',
    'name="Pick Up Address"': 'name="pickup_address"',
    'name="Delivery Address"': 'name="delivery_address"',
    'name="Message"': 'name="message"',
    'data-name="Name"': 'data-name="name"',
    'data-name="Email"': 'data-name="email"',
    'data-name="Phone"': 'data-name="phone"',
    'data-name="Preferred Contact"': 'data-name="preferred_contact"',
    'data-name="Pick Up Address"': 'data-name="pickup_address"',
    'data-name="Delivery Address"': 'data-name="delivery_address"',
    'data-name="Message"': 'data-name="message"',
}

for filepath in html_files:
    rel_path = os.path.relpath(filepath, base_dir)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original_content = content

    # --- 1. Strip Contact Form 7 Resources ---
    # Stylesheet link
    content = re.sub(
        r'<link[^>]*href="[^"]*contact-form-7/includes/css/styles_c09882a6\.css[^"]*"[^>]*/>\s*',
        '',
        content
    )
    # swv-js script tag
    content = re.sub(
        r'<script[^>]*id="swv-js"[^>]*></script>\s*',
        '',
        content
    )
    # contact-form-7-js-before block
    content = re.sub(
        r'<script[^>]*id="contact-form-7-js-before"[^>]*>.*?</script>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    # contact-form-7-js script tag
    content = re.sub(
        r'<script[^>]*id="contact-form-7-js"[^>]*></script>\s*',
        '',
        content
    )
    # wpcf7-recaptcha-js script tag
    content = re.sub(
        r'<script[^>]*id="wpcf7-recaptcha-js"[^>]*></script>\s*',
        '',
        content
    )
    # wpcf7-recaptcha-js-before block
    content = re.sub(
        r'<script[^>]*id="wpcf7-recaptcha-js-before"[^>]*>.*?</script>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    # googlesitekit-events-provider-contact-form-7-js script tag
    content = re.sub(
        r'<script[^>]*id="googlesitekit-events-provider-contact-form-7-js"[^>]*></script>\s*',
        '',
        content
    )

    # --- 2. Strip CallRail Script and Comment ---
    # Comment
    content = content.replace("<!-- CallRail WordPress Integration -->\n", "")
    content = content.replace("<!-- CallRail WordPress Integration -->", "")
    # swapjs-js script tag
    content = re.sub(
        r'<script[^>]*id="swapjs-js"[^>]*></script>\s*',
        '',
        content
    )

    # --- 3. Set Action="/thank-you/" on Standard Forms ---
    # Homepage form (name="quote")
    content = content.replace(
        '<form aria-label="Contact form" class="wpcf7-form init" data-netlify="true" data-status="init" method="POST" name="quote" novalidate="novalidate">',
        '<form aria-label="Contact form" class="wpcf7-form init" data-netlify="true" data-status="init" method="POST" name="quote" novalidate="novalidate" action="/thank-you/">'
    )
    # Contact page form (name="contact")
    content = content.replace(
        '<form aria-label="Contact form" class="wpcf7-form init" data-netlify="true" data-status="init" method="POST" name="contact" novalidate="novalidate">',
        '<form aria-label="Contact form" class="wpcf7-form init" data-netlify="true" data-status="init" method="POST" name="contact" novalidate="novalidate" action="/thank-you/">'
    )
    # Special offers form (name="estimate")
    content = content.replace(
        '<form aria-label="Contact form" class="wpcf7-form init" data-netlify="true" data-status="init" method="POST" name="estimate" novalidate="novalidate">',
        '<form aria-label="Contact form" class="wpcf7-form init" data-netlify="true" data-status="init" method="POST" name="estimate" novalidate="novalidate" action="/thank-you/">'
    )

    # --- 4. Clean up Legacy Honeypot / Spam protection elements ---
    # Match the hidden Akismet honeypot paragraph block and delete it
    content = re.sub(
        r'<p style="display: none !important;"><label>Δ.*?</script></p>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    # Match the response output div and delete it
    content = content.replace('<div aria-hidden="true" class="wpcf7-response-output"></div>', '')

    # --- 5. Clean up Form Input Names (avoiding spaces / capitalization) ---
    for old, new in field_replacements.items():
        content = content.replace(old, new)

    # --- 6. Update the Parameter Capture Script ---
    # Search for any <script> ... paramsToCapture ... </script> block and replace it
    script_pattern = re.compile(
        r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\',.*?paramsToCapture.*?</script>',
        re.DOTALL
    )
    if script_pattern.search(content):
        content = script_pattern.sub(NEW_TRACKING_SCRIPT, content)
        print(f"Updated parameter capture script in: {rel_path}")

    # --- 7. Landing Page Special Adjustments (/l/ pages) ---
    if rel_path in ["l\\index.html", "l/index.html", "l\\local-move\\index.html", "l/local-move/index.html"]:
        # A. Inject Google Tag + forwarding snippet if not already loaded
        if "google_gtagjs-js" not in content:
            content = content.replace("</head>", GTAG_INJECTION_HTML + "\n</head>")
            print(f"Injected Google gtag snippet into head of: {rel_path}")
        
        # B. Update submit AJAX handlers to redirect to /thank-you/
        old_submit_js_match = re.search(
            r'if\s*\(isValid\)\s*\{\s*const\s+submitBtn\s*=\s*form\.querySelector\(\'button\[type="submit"\]\'\);\s*if\s*\(submitBtn\)\s*\{.*?\}\s*\}',
            content,
            re.DOTALL
        )
        NEW_SUBMIT_HANDLER_JS = """          if (isValid) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
              submitBtn.textContent = '✓ Sending...';
              submitBtn.disabled = true;

              // Submit via AJAX to Netlify
              const formData = new FormData(form);
              formData.append('form-name', form.getAttribute('name'));

              fetch('/', {
                method: 'POST',
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams(formData).toString()
              })
              .then(() => {
                window.location.href = '/thank-you/';
              })
              .catch(err => {
                console.error('Form submission failed:', err);
                submitBtn.textContent = '✗ Error sending';
                submitBtn.disabled = false;
              });
            }
          }"""
        
        if old_submit_js_match:
            content = content.replace(old_submit_js_match.group(0), NEW_SUBMIT_HANDLER_JS)
            print(f"Updated AJAX submit handler to redirect to /thank-you/ in: {rel_path}")

    # --- 8. Write back changes if modified ---
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated file: {rel_path}")

print("Site-wide fixes applied.")
