#!/usr/bin/env python3

"""
Sora video generation helper

Capabilities:
1) prepare: Extract cinematic video prompts from
   04_Resources/Assets/Animations/Cinematic_Sequences.md and emit a
   machine-friendly CSV + JSON, with merged, world-adherent prompt text.

2) automate (best-effort): If Selenium is available and a ChromeDriver
   is installed, log into Sora (ChatGPT Video) and submit prompts
   automatically. This is a convenience fallback until an official API
   is available. Requires environment variables for credentials.

Usage:
  python3 scripts/generate_videos_sora.py --prepare [--limit 10]
  SORA_EMAIL=you@example.com SORA_PASSWORD='***' \
    python3 scripts/generate_videos_sora.py --automate --limit 10

Outputs:
  - 04_Resources/Assets/Animations/Generated/video_prompts.csv
  - 04_Resources/Assets/Animations/Generated/video_prompts.json

Note:
  The automate mode uses best-effort selectors that may change.
  It will open a browser, navigate to Sora/ChatGPT Video, and attempt
  to submit each prompt with requested aspect/duration. Downloading the
  finished video still requires a manual click unless configured in the
  browser profile. The script records a run log under reports/.
"""

import os, json, re, csv, time
from typing import List, Dict, Any

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
PROMPTS_MD = os.path.join(ROOT, '04_Resources', 'Assets', 'Animations', 'Cinematic_Sequences.md')
OUT_DIR = os.path.join(ROOT, '04_Resources', 'Assets', 'Animations', 'Generated')
REPORTS = os.path.join(ROOT, 'reports')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)
API_CONFIG = os.path.join(ROOT, '.obsidian', 'api_config.json')

def read_file(p: str) -> str:
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()

def extract_json_blocks(md: str) -> List[Dict[str, Any]]:
    # Find fenced code blocks with json
    blocks = []
    for m in re.finditer(r"```json\s*([\s\S]*?)\s*```", md, re.M):
        try:
            obj = json.loads(m.group(1))
            blocks.append(obj)
        except Exception:
            continue
    return blocks

def build_prompt(record: Dict[str, Any]) -> str:
    # Merge title, style, shot, action, negatives into one Sora-ready prompt
    title = record.get('title') or record.get('id') or 'Cinematic Scene'
    style = record.get('style') or ''
    shot = record.get('shot') or ''
    action = record.get('action') or ''
    negatives = record.get('negatives') or []
    neg = ''
    if isinstance(negatives, list) and negatives:
        neg = ' Avoid: ' + ', '.join(negatives) + '.'
    elif isinstance(negatives, str) and negatives.strip():
        neg = ' Avoid: ' + negatives.strip() + '.'
    # World adherence line (Aquabyssos/Aethermoor/Void aesthetic)
    world_line = 'Unified painterly fantasy realism consistent with Aquabyssos/Aethermoor/Void aesthetics; no modern signage; no sci‑fi UI; no gibberish text.'
    prompt = f"{title}. {style} Shot: {shot}. Action: {action}.{neg} {world_line}"
    return re.sub(r"\s+", " ", prompt).strip()

def write_outputs(rows: List[Dict[str, Any]]):
    # CSV
    csv_path = os.path.join(OUT_DIR, 'video_prompts.csv')
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id','title','duration_s','aspect','prompt'])
        for r in rows:
            w.writerow([r['id'], r['title'], r['duration_s'], r['aspect'], r['prompt']])
    # JSON
    json_path = os.path.join(OUT_DIR, 'video_prompts.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"prepared: {os.path.relpath(csv_path, ROOT)} ; {os.path.relpath(json_path, ROOT)}")

def do_prepare(limit: int | None):
    if not os.path.exists(PROMPTS_MD):
        print(f"missing prompts file: {os.path.relpath(PROMPTS_MD, ROOT)}")
        return
    md = read_file(PROMPTS_MD)
    blocks = extract_json_blocks(md)
    rows = []
    for i, b in enumerate(blocks):
        if limit and len(rows) >= limit:
            break
        out = {
            'id': b.get('id') or f'cin-{i+1}',
            'title': b.get('title') or f'Scene {i+1}',
            'duration_s': int(b.get('duration_s') or 10),
            'aspect': b.get('aspect') or '16:9',
            'prompt': build_prompt(b),
        }
        rows.append(out)
    if not rows:
        print('no prompts found')
        return
    write_outputs(rows)

def do_automate(limit: int | None):
    # Lazy import selenium
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    except Exception:
        print('Selenium not available. Install with: pip install selenium && ensure ChromeDriver is installed.')
        return

    # Load prepared prompts
    prompts_json = os.path.join(OUT_DIR, 'video_prompts.json')
    if not os.path.exists(prompts_json):
        print('Prompts JSON missing. Run --prepare first.')
        return
    jobs: List[Dict[str, Any]] = json.load(open(prompts_json, 'r', encoding='utf-8'))
    if limit:
        jobs = jobs[:limit]

    # Try env first
    email = os.environ.get('SORA_EMAIL') or os.environ.get('OPENAI_EMAIL')
    password = os.environ.get('SORA_PASSWORD') or os.environ.get('OPENAI_PASSWORD')
    # Try config file for optional email/password if provided
    if (not email or not password) and os.path.exists(API_CONFIG):
        try:
            cfg = json.load(open(API_CONFIG, 'r', encoding='utf-8'))
            maybe = cfg.get('openai') or {}
            email = email or maybe.get('email')
            password = password or maybe.get('password')
        except Exception:
            pass
    if not (email and password):
        print('Set SORA_EMAIL and SORA_PASSWORD env vars (or OPENAI_EMAIL/OPENAI_PASSWORD).')
        return

    # Start browser
    opts = webdriver.ChromeOptions()
    # opts.add_argument('--headless=new')  # keep visible for user review
    # Set downloads to OUT_DIR
    prefs = {
        "download.default_directory": OUT_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 30)
    log_path = os.path.join(REPORTS, 'sora_automation.log')
    log = open(log_path, 'w', encoding='utf-8')

    try:
        # Navigate to ChatGPT Video/Sora (trying both)
        targets = ['https://sora.chatgpt.com/', 'https://sora.com/', 'https://chat.openai.com']
        for url in targets:
            try:
                driver.get(url)
                time.sleep(2)
                break
            except Exception:
                continue

        # Simple login flow heuristics
        try:
            # Click a login button if visible
            buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Log In') or contains(., 'Sign in') or contains(., 'Login')]")
            if buttons:
                buttons[0].click()
                time.sleep(2)
        except Exception:
            pass

        # Try email/password fields
        try:
            email_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email' or @id='username']")))
            email_el.clear(); email_el.send_keys(email)
            pwd_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @name='password' or @id='password']")))
            pwd_el.clear(); pwd_el.send_keys(password)
            pwd_el.send_keys(Keys.RETURN)
            time.sleep(5)
        except Exception:
            pass

        # Navigate to a create/generate page
        for url in ['https://sora.com/create', 'https://sora.chatgpt.com/create']:
            try:
                driver.get(url)
                time.sleep(2)
                break
            except Exception:
                continue

        submitted = 0
        for job in jobs:
            try:
                # Find prompt textarea or input
                prompt_el = None
                for xpath in [
                    "//textarea[@name='prompt']",
                    "//textarea[contains(@placeholder, 'Describe') or contains(@placeholder, 'prompt')]",
                    "//input[@name='prompt']",
                    "//div[@role='textbox']",
                ]:
                    els = driver.find_elements(By.XPATH, xpath)
                    if els:
                        prompt_el = els[0]
                        break
                if prompt_el is None:
                    raise RuntimeError('prompt field not found')

                # Clear and type prompt
                prompt_el.clear()
                prompt_el.send_keys(job['prompt'])

                # Attempt to set duration/aspect via dropdowns or inputs if present
                for dur_xpath in [
                    "//select[@name='duration']",
                    "//input[@name='duration']",
                    "//input[contains(@placeholder,'duration')]",
                ]:
                    try:
                        el = driver.find_element(By.XPATH, dur_xpath)
                        el.clear(); el.send_keys(str(job['duration_s']))
                        break
                    except Exception:
                        pass

                for aspect_xpath in [
                    "//select[@name='aspect']",
                    "//input[@name='aspect']",
                    "//input[contains(@placeholder,'aspect')]",
                ]:
                    try:
                        el = driver.find_element(By.XPATH, aspect_xpath)
                        el.clear(); el.send_keys(job['aspect'])
                        break
                    except Exception:
                        pass

                # Click generate
                gen_btn = None
                for bx in [
                    "//button[contains(., 'Generate')]",
                    "//button[contains(., 'Create')]",
                    "//button[contains(., 'Render')]",
                ]:
                    els = driver.find_elements(By.XPATH, bx)
                    if els:
                        gen_btn = els[0]
                        break
                if gen_btn is None:
                    raise RuntimeError('generate button not found')

                gen_btn.click()
                submitted += 1
                log.write(f"submitted: {job['id']} | {job['title']}\n")
                log.flush()
                time.sleep(3)
            except Exception as e:
                log.write(f"error submitting {job.get('id')}: {e}\n")
                log.flush()

        print(f"submitted jobs: {submitted}; log: {os.path.relpath(log_path, ROOT)}")

    finally:
        try:
            log.close()
        except Exception:
            pass
        try:
            driver.quit()
        except Exception:
            pass

def parse_args():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare', action='store_true', help='extract prompts and write CSV/JSON')
    ap.add_argument('--automate', action='store_true', help='best-effort browser automation to submit prompts')
    ap.add_argument('--limit', type=int, default=None, help='limit number of prompts')
    return ap.parse_args()

def main():
    args = parse_args()
    if args.prepare:
        do_prepare(args.limit)
    if args.automate:
        do_automate(args.limit)
    if not args.prepare and not args.automate:
        print('nothing to do. Use --prepare and/or --automate.')

if __name__ == '__main__':
    main()


