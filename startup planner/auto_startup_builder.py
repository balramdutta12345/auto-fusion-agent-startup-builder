import sys
import json
from concurrent.futures import ThreadPoolExecutor
from intake_agent import intake_agent as _new_intake_agent
from research_agent import research_agent as _new_research_agent
from brand_naming_agent import brand_naming_agent as _new_brand_agent
from gtm_agent import gtm_agent as _new_gtm_agent
from website_agent import website_agent as _new_website_agent
from deliverables_agent import deliverables_agent as _new_deliverables_agent

def _infer_audience(text):
    t = text.lower()
    if any(k in t for k in ["parents","kids","families"]):
        return "families"
    if any(k in t for k in ["developers","engineers","coders"]):
        return "developers"
    if any(k in t for k in ["students","schools","education"]):
        return "students"
    if any(k in t for k in ["freelancers","creators","influencers"]):
        return "creators"
    if any(k in t for k in ["smb","small business","local business"]):
        return "SMBs"
    if any(k in t for k in ["enterprise","b2b","teams","companies"]):
        return "business teams"
    if any(k in t for k in ["professionals","busy"]):
        return "busy professionals"
    return "consumers"

def _infer_product_type(text):
    t = text.lower()
    if any(k in t for k in ["app","mobile","ios","android"]):
        return "app"
    if any(k in t for k in ["platform","marketplace"]):
        return "platform"
    if any(k in t for k in ["plugin","extension"]):
        return "plugin"
    if any(k in t for k in ["tool","assistant","bot","ai"]):
        return "tool"
    if any(k in t for k in ["service","consulting"]):
        return "service"
    return "web app"

def intake_agent(idea_text, language="English", tone_override=None):
    idea = idea_text.strip()
    audience = _infer_audience(idea)
    product_type = _infer_product_type(idea)
    top_goal = "validate demand and initial traction"
    tone = tone_override or "friendly and credible"
    price_sensitivity = "moderate"
    key_features = ["clear value proposition", "simple onboarding", "shareable output"]
    assumptions = [
        "audience inferred from idea",
        "product type inferred from keywords",
        "goal set to early traction",
        "tone set to approachable",
        "pricing sensitivity moderate"
    ]
    follow_up_question = None
    if not idea or not audience:
        follow_up_question = "Who is the primary audience?"
    brief = {
        "idea": idea,
        "primary_audience": audience,
        "product_type": product_type,
        "primary_goal": top_goal,
        "tone": tone,
        "language": language,
        "must_have_pages": ["home","about","pricing","contact"],
        "price_sensitivity": price_sensitivity,
        "key_features": key_features,
        "assumptions": assumptions,
        "success_summary": "Deliver a validated MVP concept with clear positioning and first users",
    }
    if follow_up_question:
        brief["follow_up_question"] = follow_up_question
    return brief

def research_agent(brief):
    audience = brief["primary_audience"]
    product_type = brief["product_type"]
    idea = brief["idea"]
    market_snapshot = (
        f"The {product_type} addressing {audience} focuses on the problem described as: {idea}. "
        f"Demand is driven by convenience, automation, and outcome clarity. Buying decisions favor low-friction onboarding, "
        f"transparent pricing, and demonstrable results. Market entry is feasible via niche positioning and content-led acquisition."
    )
    competitors = [
        "Competitor A: adjacent solution with broad features; differentiation via focus",
        "Competitor B: legacy tool; opportunity in modern UX and speed",
        "Competitor C: niche app; limited scalability; win with integrations",
        "Competitor D: generic marketplace; lacks personalization; win with data",
        "Competitor E: manual services; win with automation and pricing"
    ]
    opportunities = [
        "Own a niche persona and speak directly to their workflow",
        "Automate repetitive steps and show outcomes instantly",
        "Bundle templates and community signals to increase trust"
    ]
    assumptions = [
        "audience pain points align with convenience",
        "competitors have gaps in UX and automation",
        "organic acquisition is viable with content"
    ]
    confidence = 0.72
    return {
        "market_snapshot": market_snapshot,
        "competitors": competitors,
        "opportunities": opportunities,
        "assumptions": assumptions,
        "confidence": confidence
    }

def name_brand_agent(brief):
    base = brief["idea"]
    def mk(n):
        return {
            "name": n,
            "rationale": f"Relates to {base} with simple, brandable sound",
            "score": round(0.6 + (hash(n) % 40)/100, 2)
        }
    names = [
        mk("LaunchLy"), mk("SparkNest"), mk("PrimeLeap"), mk("NovaLane"), mk("FlowForge"),
        mk("IdeaPilot"), mk("VentureBeam"), mk("QuickFoundry"), mk("OrbitBase"), mk("CraftSprint"),
        mk("MintPath"), mk("BrightLoom"), mk("PeakTide"), mk("ArrowCart"), mk("BoltBay"),
        mk("TrailMint"), mk("RiseGrid"), mk("Startloom"), mk("Flecto"), mk("Shiftr")
    ]
    taglines = [
        "Start smarter, launch faster",
        "From idea to traction in days",
        "Build momentum with clarity",
        "Your shortcut to product-market fit",
        "Plan, build, and go"
    ]
    personas = [
        "Pragmatic builder: clear, direct, outcome-first",
        "Optimistic mentor: encouraging, concise, credible",
        "Data-driven operator: precise, helpful, trustworthy"
    ]
    return {"names": names, "taglines": taglines, "personas": personas}

def product_pricing_agent(brief, research):
    variants = [
        {
            "name": "MVP",
            "features": ["core workflow", "basic templates", "email support"],
            "price": "$19/mo",
            "cost_assumptions": ["hosting $0.10/user/mo", "support 1h/50 users", "no paid ads"]
        },
        {
            "name": "Plus",
            "features": ["advanced automation", "integrations", "priority support"],
            "price": "$49/mo",
            "cost_assumptions": ["hosting $0.25/user/mo", "support 1h/20 users", "light paid ads"]
        },
        {
            "name": "Premium",
            "features": ["team seats", "analytics", "concierge onboarding"],
            "price": "$129/mo",
            "cost_assumptions": ["hosting $0.50/user/mo", "support 1h/10 users", "partner commissions"]
        }
    ]
    mvp_steps = ["define niche persona", "ship core workflow", "collect 10 testimonials"]
    cost_assumptions = ["infra scales with seats", "support hours vary by tier", "ads budget small at start"]
    confidence = 0.76
    return {"variants": variants, "mvp_steps": mvp_steps, "cost_assumptions": cost_assumptions, "confidence": confidence}

def gtm_agent(brief, opportunities, personas):
    calendar = []
    for d in range(1, 31):
        if d == 1:
            action = "publish positioning and value proposition"
        elif d == 7:
            action = "release MVP to early adopters"
        elif d == 14:
            action = "share case study and collect quotes"
        elif d == 21:
            action = "launch small paid test and iterate"
        elif d == 30:
            action = "announce open beta and referral offer"
        else:
            action = "daily social and outreach"
        calendar.append({"day": d, "action": action})
    posts = []
    hashtags = "#startup #mvp #product #growth"
    for i in range(10):
        posts.append({
            "platform": "Twitter",
            "caption": f"Day {i+1}: building for {brief['primary_audience']} with a clear outcome",
            "asset_type": "image",
            "CTA": "Join early access",
            "hashtags": hashtags,
            "image_prompt": "Clean minimal graphic showing progress and speed"
        })
    press_pitch = "New tool helps a focused audience accelerate from idea to outcome using automation and templates. Early adopters report faster validation and clearer positioning. Seeking coverage on practical innovation and creator tools."
    confidence = 0.7
    return {"calendar": calendar, "posts": posts, "press_pitch": press_pitch, "confidence": confidence}

def _csv_escape(s):
    if "," in s or "\n" in s or '"' in s:
        return '"' + s.replace('"', '""') + '"'
    return s

def deliverables_agent(brief, research, brand, product, gtm):
    low_conf = []
    for k in [("research", research.get("confidence", 1.0)), ("product", product.get("confidence", 1.0)), ("gtm", gtm.get("confidence", 1.0))]:
        if k[1] < 0.6:
            low_conf.append(k[0])
    title = brand["names"][0]["name"] if brand.get("names") else "Startup"
    tagline = brand["taglines"][0] if brand.get("taglines") else ""
    onepager_md = f"# {title}\n\n{tagline}\n\n**Problem**\n\n{brief['idea']}\n\n**Solution**\n\nAutomation, clear outcomes, and templates for {brief['audience']}.\n\n**Market**\n\n{research['market_snapshot']}\n\n**Business Model**\n\nSubscription tiers: {', '.join(v['name'] for v in product['variants'])}.\n\n**Team Ask**\n\nLooking for builders and early partners.\n"
    if low_conf:
        onepager_md = "**Confidence warning: " + ", ".join(low_conf) + "**\n\n" + onepager_md
    landing_html_text = (
        f"<section class='hero'><h1>{title}</h1><p>{tagline}</p><button>Get Early Access</button></section>"+
        f"<section><h2>Features</h2><ul><li>{product['variants'][0]['features'][0]}</li><li>{product['variants'][0]['features'][1]}</li><li>{product['variants'][0]['features'][2]}</li></ul></section>"+
        f"<section><h2>How it helps</h2><p>Designed for {brief['primary_audience']} to achieve outcomes fast.</p></section>"+
        f"<section><h2>Pricing</h2><p>{', '.join(v['name']+': '+v['price'] for v in product['variants'])}</p></section>"+
        f"<meta name='title' content='{title} - {tagline}'><meta name='description' content='Plan, build, and launch faster'>"
    )
    pitch_bullets = [
        "Focuses on a clear niche audience",
        "Delivers instant value via automation",
        "Low-friction onboarding with templates",
        "Subscription model with scalable margins",
        "Early adopter momentum and content-led growth",
        "Partner-ready with integrations"
    ]
    logo_prompt = [
        f"Minimal geometric mark, modern sans-serif logotype, evokes speed and clarity for {title}",
        f"Friendly rounded mark, subtle gradient, approachable innovation vibe for {title}"
    ]
    rows = ["platform,caption,asset_type,CTA,hashtags,image_prompt"]
    for p in gtm["posts"]:
        row = ",".join([
            _csv_escape(p["platform"]),
            _csv_escape(p["caption"]),
            _csv_escape(p["asset_type"]),
            _csv_escape(p["CTA"]),
            _csv_escape(p["hashtags"]),
            _csv_escape(p.get("image_prompt","")),
        ])
        rows.append(row)
    social_csv = "\n".join(rows)
    next_steps = [
        "Day 1: finalize positioning and hero messaging",
        "Day 2: build landing and waitlist",
        "Day 3: seed 20 prospects",
        "Day 4: ship MVP core flow",
        "Day 5: collect feedback and iterate",
        "Day 6: publish case study",
        "Day 7: start referral program"
    ]
    assumptions_summary = {
        "intake": brief.get("assumptions", []),
        "research": research.get("assumptions", []),
        "notes": ["pricing sensitivities estimated", "persona tone inferred"]
    }
    confidence_summary = {
        "research": research.get("confidence", 1.0),
        "product": product.get("confidence", 1.0),
        "gtm": gtm.get("confidence", 1.0)
    }
    plain_files = {
        "onepager.md": onepager_md,
        "landing_text.html": landing_html_text,
        "social_posts.csv": social_csv,
        "logo_prompts.txt": "\n".join(logo_prompt),
        "next_steps.md": "\n".join(next_steps)
    }
    return {
        "onepager_md": onepager_md,
        "landing_html_text": landing_html_text,
        "pitch_bullets": pitch_bullets,
        "logo_prompt": logo_prompt,
        "social_csv": social_csv,
        "next_steps": next_steps,
        "assumptions_summary": assumptions_summary,
        "confidence_summary": confidence_summary,
        "plain_files": plain_files
    }

def website_agent(brief, brand, product, deliverables):
    title = brand["names"][0]["name"] if brand.get("names") else "Startup"
    tagline = brand["taglines"][0] if brand.get("taglines") else "Launch faster"
    features = product["variants"][0]["features"]
    pricing = ", ".join(v['name']+': '+v['price'] for v in product['variants'])
    index_html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title} – {tagline}</title>
  <meta name=\"description\" content=\"Plan, build, and launch faster\">
  <link rel=\"stylesheet\" href=\"styles.css\">
  <script type=\"application/ld+json\">{{\"@context\":\"https://schema.org\",\"@type\":\"Organization\",\"name\":\"{title}\"}}</script>
</head>
<body>
  <header class=\"hero\">
    <h1>{title}</h1>
    <p class=\"tagline\">{tagline}</p>
    <a class=\"cta\" href=\"#pricing\">Get Early Access</a>
  </header>
  <main>
    <section class=\"features\" aria-label=\"Features\">
      <h2>Features</h2>
      <div class=\"grid\">
        <article>
          <img src=\"assets/feature-1.png\" alt=\"Feature icon\" />
          <h3>{features[0]}</h3><p>Simple and effective.</p>
        </article>
        <article>
          <img src=\"assets/feature-2.png\" alt=\"Feature icon\" />
          <h3>{features[1]}</h3><p>Templates to start fast.</p>
        </article>
        <article>
          <img src=\"assets/feature-3.png\" alt=\"Feature icon\" />
          <h3>{features[2]}</h3><p>Support when you need it.</p>
        </article>
      </div>
    </section>
    <section id=\"pricing\" class=\"pricing\" aria-label=\"Pricing\">
      <h2>Pricing</h2>
      <p>{pricing}</p>
    </section>
    <section class=\"social-proof\" aria-label=\"Social Proof\">
      <h2>What early users say</h2>
      <ul>
        <li><blockquote>Helped me launch faster.</blockquote><cite>— Early Adopter</cite></li>
      </ul>
    </section>
    <section class=\"cta-section\" aria-label=\"Join\">
      <form class=\"email-capture\" action=\"#\" method=\"post\">
        <input type=\"email\" placeholder=\"Enter your email\" aria-label=\"Email\" />
        <button type=\"submit\" class=\"cta\">Join the waitlist</button>
      </form>
    </section>
  </main>
  <footer>
    <small>&copy; {title}</small>
    <nav aria-label=\"Social links\">
      <a href=\"#\" aria-label=\"Twitter\">Twitter</a>
      <a href=\"#\" aria-label=\"LinkedIn\">LinkedIn</a>
      <a href=\"#\" aria-label=\"Email\">Email</a>
    </nav>
  </footer>
</body>
</html>"""
    styles_css = """
:root { --bg:#0b0d12; --fg:#e8eaed; --muted:#9aa0a6; --brand:#4f8cff; }
* { box-sizing: border-box; }
body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; color: var(--fg); background: var(--bg); }
.hero { padding: 4rem 1rem; text-align:center; background: linear-gradient(135deg, #0b0d12 0%, #14213d 100%); }
.hero h1 { margin:0 0 .5rem; font-size: clamp(2rem, 5vw, 3rem); }
.tagline { color: var(--muted); margin-bottom:1rem; }
.cta { display:inline-block; padding:.75rem 1rem; background: var(--brand); color:#fff; text-decoration:none; border-radius:.5rem; }
main { max-width: 960px; margin: 0 auto; padding: 2rem 1rem; }
.features .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
.features article { padding:1rem; border: 1px solid #1f2937; border-radius:.75rem; background:#111827; }
.features img { width:48px; height:48px; display:block; margin-bottom:.5rem; opacity:.8; }
.features h3 { margin:.25rem 0 .5rem; font-size:1.1rem; }
.pricing, .social-proof, .cta-section { margin-top:2rem; }
.cta-section { text-align:center; }
.email-capture { display:flex; gap:.5rem; justify-content:center; }
.email-capture input { padding:.5rem; border-radius:.5rem; border:1px solid #1f2937; background:#0f172a; color:var(--fg); width:min(100%,280px); }
.email-capture button { padding:.5rem 1rem; }
footer { text-align:center; padding:2rem 1rem; color: var(--muted); }
footer nav { display:flex; gap:1rem; justify-content:center; margin-top:.5rem; }
@media (prefers-color-scheme: light) {
  :root { --bg:#ffffff; --fg:#111827; --muted:#6b7280; --brand:#2563eb; }
  .features article { background:#f9fafb; border-color:#e5e7eb; }
}
"""
    assets_list = [
        {"file": "assets/hero.jpg", "alt": f"Hero visual for {title}", "prompt": "Abstract geometric speed/clarity motif, soft gradient"},
        {"file": "assets/feature-1.png", "alt": "Feature icon", "prompt": "Minimal line icon of automation"},
        {"file": "assets/feature-2.png", "alt": "Feature icon", "prompt": "Minimal line icon of templates"},
        {"file": "assets/feature-3.png", "alt": "Feature icon", "prompt": "Minimal line icon of support"},
        {"file": "assets/social-proof.jpg", "alt": "Testimonials collage", "prompt": "Clean quotes layout, subtle background"}
    ]
    readme_deploy = (
        "GitHub Pages:\n"
        "1. Create a new GitHub repo, upload index.html, styles.css and other files to root.\n"
        "2. In repo Settings → Pages → Select main branch → Save → Visit https://<username>.github.io/<repo>.\n\n"
        "Netlify:\n"
        "1. Create a new site on Netlify.\n"
        "2. Drag-and-drop the 'site' folder into Netlify; publish."
    )
    confidence = 0.8
    about_html = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>About – {title}</title><link rel=\"stylesheet\" href=\"styles.css\"></head><body><main><h1>About</h1><p>Our mission is to help {brief['primary_audience']} achieve outcomes faster.</p><section><h2>Story</h2><p>Built to simplify and accelerate.</p></section><section><h2>Team</h2><p>Team info coming soon.</p></section></main></body></html>"""
    pricing_html = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Pricing – {title}</title><link rel=\"stylesheet\" href=\"styles.css\"></head><body><main><h1>Pricing</h1><ul><li>{product['variants'][0]['name']} – {product['variants'][0]['price']}</li><li>{product['variants'][1]['name']} – {product['variants'][1]['price']}</li><li>{product['variants'][2]['name']} – {product['variants'][2]['price']}</li></ul></main></body></html>"""
    contact_html = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Contact – {title}</title><link rel=\"stylesheet\" href=\"styles.css\"></head><body><main><h1>Contact</h1><p>Email us at hello@example.com</p><form action=\"mailto:hello@example.com\" method=\"post\"><input type=\"text\" placeholder=\"Your name\"><input type=\"email\" placeholder=\"Your email\"><textarea placeholder=\"Message\"></textarea><button type=\"submit\">Send</button></form></main></body></html>"""
    return {"index_html": index_html, "about_html": about_html, "pricing_html": pricing_html, "contact_html": contact_html, "styles_css": styles_css, "assets_list": assets_list, "readme_deploy": readme_deploy, "confidence": confidence}

def content_agent(brief):
    idx = {
        "hero_headline": f"{brief['idea']}",
        "subheadline": f"Designed for {brief['primary_audience']}",
        "feature_bullets": ["Fast setup","Clear outcomes","Helpful support"],
        "cta": "Get started"
    }
    about = {"mission": "Make progress simple", "story": "Built from real pains", "team": "Team to be announced"}
    pricing = {
        "tiers": [
            {"name":"MVP","price":"$19/mo","features":["core","templates","support"]},
            {"name":"Plus","price":"$49/mo","features":["automation","integrations","priority"]},
            {"name":"Premium","price":"$129/mo","features":["seats","analytics","concierge"]}
        ]
    }
    contact = {"info":"Email hello@example.com","form":"mailto"}
    blog_posts = ["Post 1", "Post 2", "Post 3"]
    testimonials = ["Placeholder testimonial 1","Placeholder testimonial 2","Placeholder testimonial 3","Placeholder testimonial 4","Placeholder testimonial 5"]
    seo_meta = {"title": brief['idea'], "description": f"{brief['idea']} for {brief['primary_audience']}"}
    return {
        "index_content": idx,
        "about_content": about,
        "pricing_content": pricing,
        "contact_content": contact,
        "blog_posts": blog_posts,
        "testimonials": testimonials,
        "seo_meta": seo_meta
    }

def seo_accessibility_agent(brief, content):
    meta = {
        "index": {"title": content["seo_meta"]["title"], "description": content["seo_meta"]["description"]},
        "about": {"title": "About", "description": "About the project"},
        "pricing": {"title": "Pricing", "description": "Plans and pricing"},
        "contact": {"title": "Contact", "description": "Reach out"},
        "og": {"title": content["seo_meta"]["title"], "description": content["seo_meta"]["description"], "image": "assets/hero.jpg"},
        "twitter": {"card": "summary_large_image", "image": "assets/hero.jpg"},
        "jsonld": {"@context":"https://schema.org","@type":"WebSite","name": content["seo_meta"]["title"]}
    }
    checklist = ["Alt text added", "ARIA labels on sections", "High contrast colors"]
    return {"meta": meta, "accessibility_checklist": checklist, "confidence": 0.78}

def run_pipeline(idea_text, language="English", tone_override=None):
    intake = fusion_intake_agent(idea_text, language, tone_override)
    def run_research():
        return fusion_research_agent(intake)
    def run_brand():
        return fusion_brand_agent(intake, None)
    def run_product():
        return fusion_product_agent(intake, None)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(run_research), ex.submit(run_brand), ex.submit(run_product)]
        research, brand, product = [f.result() for f in futs]
    gtm = fusion_gtm_agent(intake, research, brand, product)
    website = fusion_website_agent(brand, product, gtm, intake)
    deliverables = fusion_deliverables_agent(intake, research, brand, product, gtm, website)
    return {
        "intake": intake,
        "research": research,
        "brand": brand,
        "product": product,
        "gtm": gtm,
        "website": website,
        "deliverables": deliverables
    }

def main():
    if len(sys.argv) < 2:
        print("Provide a one-line startup idea as an argument")
        sys.exit(1)
    idea_text = sys.argv[1]
    out_path = None
    site_dir = None
    export_dir = None
    approve = False
    # args: IDEA [--out path] [--site-dir dir] [--export-dir dir] [--approve]
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--out" and i+1 < len(sys.argv):
            out_path = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--site-dir" and i+1 < len(sys.argv):
            site_dir = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--export-dir" and i+1 < len(sys.argv):
            export_dir = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--approve":
            approve = True
            i += 1
        elif sys.argv[i] == "--language" and i+1 < len(sys.argv):
            language = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--tone" and i+1 < len(sys.argv):
            tone = sys.argv[i+1]
            i += 2
        else:
            i += 1
    language = locals().get("language","English")
    tone = locals().get("tone", None)
    result = run_pipeline(idea_text, language, tone)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(out_path)
    else:
        print(json.dumps(result, indent=2))
    if site_dir:
        import os
        os.makedirs(site_dir, exist_ok=True)
        os.makedirs(os.path.join(site_dir, "assets"), exist_ok=True)
        wf = result["deliverables"]["website_files"]
        with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(wf["index_html"])
        if "about_html" in wf:
            with open(os.path.join(site_dir, "about.html"), "w", encoding="utf-8") as f:
                f.write(wf["about_html"])
        if "pricing_html" in wf:
            with open(os.path.join(site_dir, "pricing.html"), "w", encoding="utf-8") as f:
                f.write(wf["pricing_html"])
        if "contact_html" in wf:
            with open(os.path.join(site_dir, "contact.html"), "w", encoding="utf-8") as f:
                f.write(wf["contact_html"])
        with open(os.path.join(site_dir, "styles.css"), "w", encoding="utf-8") as f:
            f.write(wf["styles_css"])
        with open(os.path.join(site_dir, "README_deploy.txt"), "w", encoding="utf-8") as f:
            f.write(wf["readme_deploy"])
        with open(os.path.join(site_dir, "assets", "PLACEHOLDERS.txt"), "w", encoding="utf-8") as f:
            for a in wf["assets_list"]:
                f.write(f"{a['file']} | alt={a['alt']} | prompt={a['prompt']}\n")
    if approve and export_dir:
        import os
        os.makedirs(export_dir, exist_ok=True)
        files = result["deliverables"]["files"]
        for name, content in files.items():
            if name.endswith('.html') or name.endswith('.css') or name.endswith('.md') or name.endswith('.txt') or name.endswith('.csv'):
                with open(os.path.join(export_dir, name), "w", encoding="utf-8") as f:
                    f.write(content)
        site_path = os.path.join(export_dir, "site")
        os.makedirs(site_path, exist_ok=True)
        os.makedirs(os.path.join(site_path, "assets"), exist_ok=True)
        # write website files into site folder from files dict
        for name in ["index.html","about.html","pricing.html","contact.html","styles.css","README_deploy.txt"]:
            with open(os.path.join(site_path, name), "w", encoding="utf-8") as f:
                f.write(files[name])
        with open(os.path.join(site_path, "assets", "PLACEHOLDERS.txt"), "w", encoding="utf-8") as f:
            f.write(files.get("assets_prompts.txt",""))
        with open(os.path.join(export_dir, "zip_structure.txt"), "w", encoding="utf-8") as f:
            f.write(files.get("zip_structure.txt",""))
        print(export_dir)

if __name__ == "__main__":
    main()
def fusion_intake_agent(raw_idea, language="EN", tone=None):
    idea = raw_idea.strip()
    audience = _infer_audience(idea)
    goal = "launch and validate sales"
    t = tone or "friendly"
    assumptions = ["audience inferred from idea", "goal set to launch/validation", "tone default friendly"]
    follow_up = None
    if not audience or not goal:
        follow_up = "Who is the target audience or primary goal?"
    return {
        "idea": idea,
        "target_audience": audience,
        "primary_goal": goal,
        "tone": t,
        "language": language,
        "assumptions": assumptions,
        **({"follow_up_question": follow_up} if follow_up else {})
    }

def fusion_research_agent(intake):
    idea = intake["idea"]
    audience = intake["target_audience"]
    market_snapshot = f"For {audience}, the concept '{idea}' benefits from convenience and clarity. Buying decisions hinge on price, trust, and availability. Opportunity exists in niche positioning and direct outreach."
    competitors = [
        {"name":"Local incumbent","note":"Trust and availability; improve with UX and clarity"},
        {"name":"Online marketplace","note":"Wide selection; compete via curated experience"},
        {"name":"Subscription provider","note":"Recurring model; win with flexibility and pricing"}
    ]
    opportunities = [
        "Own a specific niche persona and message directly",
        "Automate ordering and updates",
        "Bundle with simple perks to raise retention"
    ]
    assumptions = ["pricing sensitivity moderate", "organic content viable", "logistics manageable at small scale"]
    return {"market_snapshot": market_snapshot, "competitors": competitors, "opportunities": opportunities, "assumptions": assumptions, "confidence": 0.72}

def fusion_brand_agent(intake, research):
    base = intake["idea"]
    def mk(n,i):
        return {"name": n, "rationale": f"Relates to {base}", "score": round(0.6 + (i%35)/100,2)}
    names = [mk(n,i) for i,n in enumerate(["MilkMate","FreshFlow","DairyDash","PurePour","CampusMilk","SwiftDairy","MorningPour","CreamLine","Milkloop","Udderly","WhiteWave","DailyDairy","FarmFresh","Milkly","PourJoy"])]
    taglines = ["Fresh to your door", "Simple, pure, daily", "Subscription freshness", "Better mornings, better milk", "Campus-ready dairy"]
    colors = {"primary":"#2563EB","secondary":"#111827","accent":"#F59E0B"}
    font_stack = "system-ui, -apple-system, Segoe UI, Roboto, Arial"
    logo_prompts = [
        f"Minimal droplet mark with modern sans-serif for {names[0]['name']}",
        f"Rounded carton icon, friendly tone for {names[0]['name']}"
    ]
    assumptions = ["colors chosen for contrast", "web-safe font stack", "name candidates brandable"]
    return {"names": names, "taglines": taglines, "colors": colors, "font_stack": font_stack, "logo_prompts": logo_prompts, "assumptions": assumptions, "confidence": 0.78}

def fusion_product_agent(intake, research):
    variants = [
        {"name":"MVP","features":["daily/alternate-day delivery","basic account","email support"],"price_suggested":"$19/mo"},
        {"name":"Plus","features":["custom schedule","mobile updates","priority support"],"price_suggested":"$49/mo"},
        {"name":"Premium","features":["bulk campus plans","analytics","concierge"],"price_suggested":"$129/mo"}
    ]
    mvp_steps = ["define niche (e.g., dorms)", "set ordering workflow", "collect first 20 subscribers"]
    assumptions = ["costs scale with delivery volume", "support hours per user low", "ads light initially"]
    return {"variants": variants, "mvp_steps": mvp_steps, "assumptions": assumptions, "confidence": 0.76}

def fusion_gtm_agent(intake, research, brand, product):
    launch = []
    for d in range(1,31):
        if d==1: action="announce offer and value"
        elif d==7: action="pilot deliveries to early adopters"
        elif d==14: action="share testimonials and adjust"
        elif d==21: action="run small paid test"
        elif d==30: action="open broader signups"
        else: action="daily social and outreach"
        launch.append({"day": d, "action": action})
    posts = []
    tags = "#fresh #local #subscription #students"
    for i in range(10):
        posts.append({
            "platform":"Twitter",
            "caption": f"Day {i+1}: serving {intake['target_audience']} — {intake['idea']}",
            "image_prompt":"Clean minimal graphic (milk/campus)",
            "hashtags": tags
        })
    press_pitch = "Local, fresh subscription tailored to students, delivering consistent quality and convenience. Seeking coverage on practical campus services and micro-subscription innovation."
    assumptions = ["organic reach via campus content", "DMs and flyers viable", "referrals effective"]
    return {"launch_30_days": launch, "social_posts": posts, "press_pitch": press_pitch, "assumptions": assumptions, "confidence": 0.7}

def fusion_website_agent(brand, product, gtm, intake):
    title = brand["names"][0]["name"]
    tagline = brand["taglines"][0]
    colors = brand["colors"]
    font = brand["font_stack"]
    def page_head(tt,desc):
        return f"<meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{tt}</title><meta name='description' content='{desc}'><link rel='stylesheet' href='styles.css'>"
    index_head = page_head(f"{title} – {tagline}", f"{intake['idea']} for {intake['target_audience']}") + f"<script type='application/ld+json'>{{\"@context\":\"https://schema.org\",\"@type\":\"Organization\",\"name\":\"{title}\"}}</script>"
    index_html = f"""<!doctype html><html lang='en'><head>{index_head}</head><body><header class='hero'><h1>{title}</h1><p class='tagline'>{tagline}</p><a class='cta' href='#pricing'>Get Early Access</a></header><main><section class='features' aria-label='Features'><h2>Features</h2><div class='grid'><article><img src='assets/feature-1.png' alt='Feature icon'><h3>{product['variants'][0]['features'][0]}</h3><p>Simple and effective.</p></article><article><img src='assets/feature-2.png' alt='Feature icon'><h3>{product['variants'][1]['features'][0]}</h3><p>Flexible and clear.</p></article><article><img src='assets/feature-3.png' alt='Feature icon'><h3>{product['variants'][2]['features'][0]}</h3><p>Scale when ready.</p></article></div></section><section id='pricing' class='pricing' aria-label='Pricing'><h2>Pricing</h2><ul><li>{product['variants'][0]['name']} – {product['variants'][0]['price_suggested']}</li><li>{product['variants'][1]['name']} – {product['variants'][1]['price_suggested']}</li><li>{product['variants'][2]['name']} – {product['variants'][2]['price_suggested']}</li></ul></section><section class='cta-section' aria-label='Join'><form class='email-capture' action='#' method='post'><input type='email' placeholder='Enter your email' aria-label='Email'><button type='submit' class='cta'>Join the waitlist</button></form></section></main><footer><small>&copy; {title}</small></footer></body></html>"""
    about_html = f"<!doctype html><html lang='en'><head>{page_head('About – '+title,'About '+title)}</head><body><main><h1>About</h1><section><h2>Mission</h2><p>Serve {intake['target_audience']} with fresh convenience.</p></section><section><h2>Story</h2><p>Born from the need for reliable, student-friendly subscriptions.</p></section></main></body></html>"
    pricing_html = f"<!doctype html><html lang='en'><head>{page_head('Pricing – '+title,'Pricing')}</head><body><main><h1>Pricing</h1><ul><li>{product['variants'][0]['name']} – {product['variants'][0]['price_suggested']}</li><li>{product['variants'][1]['name']} – {product['variants'][1]['price_suggested']}</li><li>{product['variants'][2]['name']} – {product['variants'][2]['price_suggested']}</li></ul></main></body></html>"
    contact_html = f"<!doctype html><html lang='en'><head>{page_head('Contact – '+title,'Contact')}</head><body><main><h1>Contact</h1><p>Email us at hello@example.com</p><form action='mailto:hello@example.com' method='post'><input type='text' placeholder='Your name'><input type='email' placeholder='Your email'><textarea placeholder='Message'></textarea><button type='submit'>Send</button></form></main></body></html>"
    styles_css = f":root {{ --bg:{colors['secondary']}; --fg:#e8eaed; --muted:#9aa0a6; --brand:{colors['primary']}; --accent:{colors['accent']}; }}\n* {{ box-sizing: border-box; }}\nbody {{ margin:0; font-family: {font}; color: var(--fg); background: var(--bg); }}\n.hero {{ padding: 4rem 1rem; text-align:center; background: linear-gradient(135deg, var(--secondary,#0b0d12) 0%, #14213d 100%); }}\n.hero h1 {{ margin:0 0 .5rem; font-size: clamp(2rem, 5vw, 3rem); }}\n.tagline {{ color: var(--muted); margin-bottom:1rem; }}\n.cta {{ display:inline-block; padding:.75rem 1rem; background: var(--brand); color:#fff; text-decoration:none; border-radius:.5rem; }}\nmain {{ max-width: 960px; margin: 0 auto; padding: 2rem 1rem; }}\n.features .grid {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}\n.features article {{ padding:1rem; border: 1px solid #1f2937; border-radius:.75rem; background:#111827; }}\n.features img {{ width:48px; height:48px; display:block; margin-bottom:.5rem; opacity:.8; }}\n.features h3 {{ margin:.25rem 0 .5rem; font-size:1.1rem; }}\n.pricing, .cta-section {{ margin-top:2rem; }}\n.email-capture {{ display:flex; gap:.5rem; justify-content:center; }}\n.email-capture input {{ padding:.5rem; border-radius:.5rem; border:1px solid #1f2937; background:#0f172a; color:var(--fg); width:min(100%,280px); }}\n.email-capture button {{ padding:.5rem 1rem; }}\nfooter {{ text-align:center; padding:2rem 1rem; color: var(--muted); }}\n@media (prefers-color-scheme: light) {{ :root {{ --bg:#ffffff; --fg:#111827; --muted:#6b7280; --brand:{colors['primary']}; }} .features article {{ background:#f9fafb; border-color:#e5e7eb; }} }}"
    assets_list = [
        {"filename":"assets/hero.jpg","alt_text":f"Hero visual for {title}","prompt":"Droplet/cream motif","size":"1200x800"},
        {"filename":"assets/feature-1.png","alt_text":"Feature icon","prompt":"Minimal line icon","size":"256x256"},
        {"filename":"assets/feature-2.png","alt_text":"Feature icon","prompt":"Minimal line icon","size":"256x256"},
        {"filename":"assets/feature-3.png","alt_text":"Feature icon","prompt":"Minimal line icon","size":"256x256"}
    ]
    assumptions = ["pages tailored to idea", "JSON-LD present", "pure static site"]
    return {"index_html": index_html, "about_html": about_html, "pricing_html": pricing_html, "contact_html": contact_html, "styles_css": styles_css, "assets_list": assets_list, "assumptions": assumptions, "confidence": 0.8}

def fusion_deliverables_agent(intake, research, brand, product, gtm, website):
    needs = []
    for name,val in [("research",research["confidence"]),("brand",brand["confidence"]),("product",product["confidence"]),("gtm",gtm["confidence"]),("website",website["confidence"])]:
        if val < 0.6:
            needs.append(name)
    files = {
        "index.html": website["index_html"],
        "about.html": website["about_html"],
        "pricing.html": website["pricing_html"],
        "contact.html": website["contact_html"],
        "styles.css": website["styles_css"],
        "assets_prompts.txt": "\n".join(f"{a['filename']} | alt={a['alt_text']} | prompt={a['prompt']} | size={a['size']}" for a in website["assets_list"]),
        "social_posts.csv": "\n".join([
            "platform,caption,image_prompt,hashtags" 
        ] + [ ",".join([
            p["platform"],
            p["caption"].replace(","," "),
            p["image_prompt"].replace(","," "),
            p["hashtags"].replace(","," ")
        ]) for p in gtm["social_posts"] ]),
        "logo_prompts.txt": "\n".join(brand["logo_prompts"]),
        "onepager.md": f"# {brand['names'][0]['name']}\n\n{brand['taglines'][0]}\n\n**Idea**\n\n{intake['idea']}\n\n**Audience**\n\n{intake['target_audience']}\n\n**Market**\n\n{research['market_snapshot']}\n\n**Product**\n\n"+"; ".join(v['name'] for v in product['variants'])+"\n",
        "README_deploy.txt": "GitHub Pages:\n1. Create a new GitHub repo, upload index.html, styles.css and other files to root.\n2. In repo Settings → Pages → Select main branch → Save → Visit https://<username>.github.io/<repo>.\n\nNetlify:\n1. Create a new site on Netlify.\n2. Drag-and-drop the 'site' folder into Netlify; publish.",
        "zip_structure.txt": "\n".join(["site/index.html","site/about.html","site/pricing.html","site/contact.html","site/styles.css","site/assets/","site/README_deploy.txt"])
    }
    assumptions_and_confidence = {
        "intake": intake.get("assumptions",[]),
        "research": research.get("assumptions",[]),
        "brand": brand.get("assumptions",[]),
        "product": product.get("assumptions",[]),
        "gtm": gtm.get("assumptions",[]),
        "website": website.get("assumptions",[]),
        "confidence": {
            "research": research["confidence"],
            "brand": brand["confidence"],
            "product": product["confidence"],
            "gtm": gtm["confidence"],
            "website": website["confidence"]
        }
    }
    return {"files": files, "assumptions_and_confidence": assumptions_and_confidence, "needs_review_flags": needs, "export_ready": True}
FALLBACK = "NOTHING WORKING — NO OUTPUTS"

def req_intake_agent(raw_idea, language="EN", tone=None):
    idea = (raw_idea or "").strip()
    audience = _infer_audience(idea) if idea else None
    primary_goal = "launch and validate traction"
    t = tone or "friendly"
    assumptions = ["audience inferred from idea if present", "goal defaulted to launch validation", "tone default friendly"]
    follow_up = None
    if not audience or not primary_goal:
        follow_up = "Who is the target audience or primary goal?"
    return {
        "idea": idea or FALLBACK,
        "target_audience": audience or FALLBACK,
        "primary_goal": primary_goal or FALLBACK,
        "tone": t,
        "language": language,
        "assumptions": assumptions,
        **({"follow_up_question": follow_up} if follow_up else {})
    }

def req_research_agent(intake):
    try:
        if intake.get("idea") == FALLBACK:
            raise ValueError("no idea")
        audience = intake.get("target_audience", FALLBACK)
        idea = intake.get("idea", FALLBACK)
        market_snapshot = f"For {audience}, the idea '{idea}' is driven by convenience, price, and trust. Entry via clear positioning and direct outreach." if audience != FALLBACK else FALLBACK
        top_competitors = [{"name":"Local providers","why_relevant":"Trust and availability"},{"name":"Marketplaces","why_relevant":"Broad choice"}] if audience != FALLBACK else FALLBACK
        key_opportunities = ["Own a niche persona","Automate ordering","Bundle perks for retention"] if audience != FALLBACK else FALLBACK
        assumptions = ["pricing sensitivity moderate","organic content viable","logistics manageable"]
        confidence = 0.72
        return {
            "market_snapshot": market_snapshot if market_snapshot else FALLBACK,
            "top_competitors": top_competitors if top_competitors else FALLBACK,
            "key_opportunities": key_opportunities if key_opportunities else FALLBACK,
            "assumptions": assumptions,
            "confidence": confidence
        }
    except Exception:
        return {"market_snapshot": FALLBACK, "top_competitors": FALLBACK, "key_opportunities": FALLBACK, "assumptions": ["no inputs"], "confidence": 0.4}

def req_brand_agent(intake, research):
    try:
        base = intake.get("idea", FALLBACK)
        if base == FALLBACK:
            raise ValueError("no idea")
        def mk(n,i):
            return {"name": n, "rationale": f"Relates to {base}", "score": round(0.6 + (i%35)/100,2)}
        names_raw = ["BrightCart","FlowMilk","PurePath","FreshStep","MorningMaze","SwiftPour","CampusFresh","DailyDash","CreamLine","WhiteWave"]
        names = [mk(n,i) for i,n in enumerate(names_raw)]
        taglines = ["Fresh made simple","Ready for every day","Quality you can count","Subscription freshness","Better mornings"]
        chosen_name = names[0]["name"]
        color_palette = {"primary":"#2563EB","secondary":"#111827","accent":"#F59E0B"}
        font_stack = "system-ui, -apple-system, Segoe UI, Roboto, Arial"
        logo_prompt = f"Minimal droplet, modern sans-serif logotype for {chosen_name}"
        assumptions = ["palette chosen for contrast","web-safe font stack"]
        return {"names": names, "taglines": taglines, "chosen_name": chosen_name, "color_palette": color_palette, "logo_prompt": logo_prompt, "assumptions": assumptions, "confidence": 0.78}
    except Exception:
        return {"names": FALLBACK, "taglines": FALLBACK, "chosen_name": FALLBACK, "color_palette": FALLBACK, "logo_prompt": FALLBACK, "assumptions": ["no inputs"], "confidence": 0.4}

def req_product_pricing_agent(intake, research, brand):
    try:
        variants = [
            {"variant_name":"MVP","size_options":"S/M/L","features":["basic subscription","weekly delivery","email support"]},
            {"variant_name":"Plus","size_options":"S/M/L","features":["custom schedule","mobile updates","priority support"]},
            {"variant_name":"Premium","size_options":"S/M/L","features":["bulk plans","analytics","concierge"]}
        ]
        pricing = [
            {"variant_name":"MVP","price_currency":"USD","suggested_price":"19","price_rationale":"entry tier for validation"},
            {"variant_name":"Plus","price_currency":"USD","suggested_price":"49","price_rationale":"features for flexibility"},
            {"variant_name":"Premium","price_currency":"USD","suggested_price":"129","price_rationale":"team/campus scaling"}
        ]
        cost_assumptions = ["infra scales with seats","support hours vary by tier","ads budget small at start"]
        mvp_pricing_recommendation = "Start with MVP at $19/mo, test conversion, then upsell to Plus."
        return {"sizes_and_variants": variants, "pricing": pricing, "cost_assumptions": cost_assumptions, "mvp_pricing_recommendation": mvp_pricing_recommendation, "confidence": 0.76}
    except Exception:
        return {"sizes_and_variants": FALLBACK, "pricing": FALLBACK, "cost_assumptions": FALLBACK, "mvp_pricing_recommendation": FALLBACK, "confidence": 0.4}

def req_gtm_agent(intake, research, brand, product):
    try:
        plan = []
        for d in range(1,31):
            if d==1: action="announce offer and value"
            elif d==7: action="pilot to early adopters"
            elif d==14: action="share testimonials"
            elif d==21: action="run small paid test"
            elif d==30: action="open broader signups"
            else: action="daily social and outreach"
            plan.append({"day": d, "action": action})
        priority_channels = [
            {"channel":"Instagram","reason":"visual appeal","score":0.7},
            {"channel":"TikTok","reason":"campus reach","score":0.75},
            {"channel":"Campus flyers","reason":"local trust","score":0.6}
        ]
        social_posts_brief = [{"day":i+1,"platform":"Twitter","caption_brief":f"Day {i+1}: building for {intake.get('target_audience','users')}"} for i in range(10)]
        press_pitch_3_sentences = "Local, fresh subscription tailored to a clear audience. Early adopters report convenience and trust. Seeking coverage on practical micro-subscriptions and campus services."
        return {"launch_30_day_plan": plan, "priority_channels": priority_channels, "social_posts_brief": social_posts_brief, "press_pitch_3_sentences": press_pitch_3_sentences, "confidence": 0.7}
    except Exception:
        return {"launch_30_day_plan": FALLBACK, "priority_channels": FALLBACK, "social_posts_brief": FALLBACK, "press_pitch_3_sentences": FALLBACK, "confidence": 0.4}

def req_deliverables_agent(intake, research, brand, product, gtm):
    needs = []
    for aid, conf in [("research", research.get("confidence",0)), ("brand", brand.get("confidence",0)), ("product", product.get("confidence",0)), ("gtm", gtm.get("confidence",0))]:
        if conf < 0.6:
            needs.append({"agent_id": aid, "reason": "confidence below threshold", "confidence": conf})
    deliverables = {
        "market_research": research if research else FALLBACK,
        "brand_and_naming": brand if brand else FALLBACK,
        "product_pricing": product if product else FALLBACK,
        "launch_30_day_plan": gtm if gtm else FALLBACK,
        "assumptions_and_confidence": {
            "intake": intake.get("assumptions",[]),
            "research": research.get("assumptions",[]),
            "brand": brand.get("assumptions",[]),
            "product": product.get("cost_assumptions",[]) or product.get("assumptions",[]),
            "gtm": ["channels chosen for audience", "organic content viable"]
        },
        "needs_review_flags": needs,
        "export_ready": True
    }
    def _is_fallback(agent_id, agent):
        fields = {
            "research": ["market_snapshot"],
            "brand": ["chosen_name","taglines"],
            "product": ["pricing","sizes_and_variants"],
            "gtm": ["launch_30_day_plan"],
        }
        for k in fields.get(agent_id, []):
            v = agent.get(k)
            if isinstance(v, str) and v == FALLBACK:
                return True
        return False
    def _recovery_options(agent_id, intake_obj):
        intake_json = json.dumps(intake_obj, ensure_ascii=False)
        auto_retry_hint = f"Regenerate: be more specific and use concrete local assumptions; reference intake: {intake_json}."
        if agent_id == "research":
            question = "Which region should we focus on (city/campus)?"
        elif agent_id == "brand":
            question = "Do you prefer playful or professional tone for names?"
        elif agent_id == "product":
            question = "What is the target price range for the MVP tier?"
        elif agent_id == "gtm":
            question = "Which primary channels should we prioritize (e.g., Instagram/TikTok/Email)?"
        else:
            question = "Which audience or goal should we optimize for?"
        return {"auto_retry_hint": auto_retry_hint, "user_question": question}
    enriched = []
    for flag in needs:
        aid = flag.get("agent_id")
        agent = {"research":research,"brand":brand,"product":product,"gtm":gtm}.get(aid,{})
        if not _is_fallback(aid, agent):
            extra = _recovery_options(aid, intake)
            f = dict(flag)
            f.update(extra)
            enriched.append(f)
        else:
            enriched.append(flag)
    deliverables["needs_review_flags"] = enriched
    # ensure required keys never missing
    for k in ["market_research","brand_and_naming","product_pricing","launch_30_day_plan","assumptions_and_confidence","needs_review_flags","export_ready"]:
        if deliverables.get(k) is None:
            deliverables[k] = FALLBACK
    return deliverables

def run_required_pipeline(idea_text, language="EN", tone_override=None):
    lang = (language or "en").lower()
    if lang in ("en","english","EN"): lang = "en"
    elif lang in ("hi","hindi","HI"): lang = "hi"
    else: lang = "en"
    tone = tone_override or "casual"
    intake = _new_intake_agent(idea_text, lang, tone)
    research = _new_research_agent(intake)
    brand_payload = {
        "idea": intake.get("idea"),
        "target_audience": intake.get("target_audience"),
        "market_snapshot": research.get("market_snapshot"),
        "key_opportunities": research.get("key_opportunities"),
        "tone": intake.get("tone")
    }
    brand = _new_brand_agent(brand_payload)
    product = req_product_pricing_agent(intake, research, brand)
    gtm = _new_gtm_agent({
        "idea": intake.get("idea"),
        "target_audience": intake.get("target_audience"),
        "tone": intake.get("tone"),
        "chosen_name": brand.get("chosen_name")
    })
    # Construct minimal website content from brand/product/gtm
    features_src = product.get("sizes_and_variants") or []
    feats = []
    for i, v in enumerate(features_src[:3]):
        t = v.get("variant_name") or v.get("name") or f"Tier {i+1}"
        d = ", ".join(v.get("features", [])[:3]) if isinstance(v.get("features"), list) else "Core features"
        feats.append({"title": t, "desc": d})
    landing = {
        "hero": {"title": brand.get("chosen_name") or intake.get("idea"), "subtitle": (brand.get("taglines") or ["Ready every day"])[0]},
        "features": feats,
        "cta": {"text": "See pricing", "href": "pricing.html"}
    }
    pricing_list = []
    for pr in (product.get("pricing") or [])[:3]:
        pricing_list.append({
            "name": pr.get("variant_name") or "Tier",
            "price": (pr.get("price_currency") or "USD") + " " + str(pr.get("suggested_price") or ""),
            "features": ["core", "support"]
        })
    website = _new_website_agent({
        "landing_content": landing,
        "about_content": "We help founders move from idea to traction.",
        "pricing_content": pricing_list,
        "contact_content": {"email": "hello@example.com"},
        "brand_palette": brand.get("color_palette"),
        "font_stack": (brand.get("font_stack") or "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"),
        "assets_prompts": {"hero": (brand.get("logo_prompts") or ["Minimal geometric mark"])[0]}
    })
    # Build export deliverables from new agent
    export = _new_deliverables_agent({
        "intake": intake,
        "research": research,
        "brand": brand,
        "product": {"pricing": product.get("pricing"), "sizes_and_variants": product.get("sizes_and_variants"), "mvp_pricing_recommendation": product.get("mvp_pricing_recommendation"), "assumptions": product.get("cost_assumptions"), "confidence": product.get("confidence")},
        "gtm": gtm,
        "website": website
    })
    # Compose legacy-style deliverables for UI while including files
    needs = []
    for aid, conf in [("research", research.get("confidence",0)), ("brand", brand.get("confidence",0)), ("product", product.get("confidence",0)), ("gtm", gtm.get("confidence",0)), ("website", website.get("confidence",0))]:
        if conf < 0.6:
            needs.append({"agent_id": aid, "reason": "confidence below threshold", "confidence": conf})
    # Merge recovery hints from export
    if isinstance(export.get("needs_review_flags"), list) and export["needs_review_flags"]:
        needs = export["needs_review_flags"]
    deliverables = {
        "market_research": research,
        "brand_and_naming": brand,
        "product_pricing": product,
        "launch_30_day_plan": gtm,
        "assumptions_and_confidence": export.get("assumptions_and_confidence", {
            "intake": intake.get("assumptions",[]),
            "research": research.get("assumptions",[]),
            "brand": brand.get("assumptions",[]),
            "product": product.get("cost_assumptions",[]) or product.get("assumptions",[]),
            "gtm": gtm.get("assumptions",[]),
            "website": website.get("assumptions",[])
        }),
        "needs_review_flags": needs,
        "export_ready": True,
        "files": export.get("files")
    }
    return {"intake": intake, "research": research, "brand": brand, "product": product, "gtm": gtm, "website": website, "deliverables": deliverables}