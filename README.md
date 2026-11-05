# 🏒 PuckMetrics: Self-Hosted Fantasy Hockey Hub

[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Unraid](https://img.shields.io/badge/unraid-compatible-orange.svg)](https://unraid.net/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![TailwindCSS](https://img.shields.io/badge/frontend-TailwindCSS-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A self-hosted, modern analytics web dashboard designed for **Unraid** and **Docker** that bridges your **Yahoo Fantasy Hockey League** with the **Official NHL API**.

Unlike default platforms that push pre-draft ranks and arbitrary algorithms, **PuckMetrics completely eliminates Yahoo rank bias**. It scans your specific league settings, evaluates real on-ice statistical production, and calculates objective **Custom Value Scores** and **Off-Night Streaming Ratings** to help you dominate your waiver wire and matchups.

---

## 🌟 Key Features

- **🛡️ Zero Yahoo Rank Bias**: Ranks and suggestions are calculated mathematically using real player statistics ($Z$-score normalization for Categories, custom coefficient points for Points leagues).
- **📅 Off-Night Schedule Optimizer**: Automatically flags low-volume NHL game days (Mondays, Wednesdays, Fridays, Sundays). Prioritizes waiver wire streamers who play when your starting roster has open slots, ensuring no games are wasted on your bench.
- **⚡ Category Battleground & Deficit Alerts**: Instantly visualizes which categories your team is losing in your current Head-to-Head matchup (e.g. Shots, Hits, Blocks) and suggests available Free Agents tailored to flip those categories.
- **🔄 1-to-1 Radar Comparisons**: Compare any waiver wire target directly against any player on your active roster with interactive statistical radar overlays.
- **🔒 Secure Local Login**: Protected with master password authentication and session management—safe to expose to your local network or reverse proxy (Cloudflare Tunnels, Tailscale, Nginx, Traefik).
- **🚀 Unraid & Docker Ready**: Features a dedicated Unraid Community Applications XML template, Docker Compose file, and persistent volume mapping for `/data`.

---

## 🖥️ Screenshots & Interface

```
+-----------------------------------------------------------------------------------------+
| PuckMetrics [Unraid Edition]                 [H2H Categories]  [Demo Data]  [Settings]  |
+-----------------------------------------------------------------------------------------+
| MATCHUP WEEK 6: The Great Eight (8) vs Puck Dynasty (5)                                 |
| Target Alert: Trailing in SOG (-14), HIT (-32). Filter Waiver Wire -> [Find Free Agents]|
+-----------------------------------------------------------------------------------------+
| [Custom-Ranked Waiver Wire]                                                             |
|                                                                                         |
| #1 Wyatt Johnston (DAL - C,RW)        #2 Gabriel Vilardi (WPG - RW)                     |
| Custom Value: 89.2/100                Custom Value: 86.5/100                            |
| Stream Rating: 84.0 pts               Stream Rating: 78.0 pts                           |
| 4 Games This Week (3 Off-Nights!)     4 Games This Week (2 Off-Nights)                  |
| [Compare with Roster]                 [Compare with Roster]                             |
+-----------------------------------------------------------------------------------------+
```

---

## 🚀 Quick Start (Docker Compose)

Clone the repository and spin up the container:

```bash
git clone https://github.com/YOUR_USERNAME/fantasy-hockey-dashboard.git
cd fantasy-hockey-dashboard

# Copy environment template
cp .env.example .env

# Edit .env and set your ADMIN_PASSWORD and SECRET_KEY
nano .env

# Start container
docker-compose up -d
```

Open your browser at **`http://localhost:8585`** (or your server's IP).

---

## 🎛️ Unraid Installation

### Method 1: Using the Unraid Template
1. In your Unraid WebGUI, ensure the **Community Applications** plugin is installed.
2. Place `unraid-template.xml` into your flash drive at:
   ```
   /boot/config/plugins/dockerMan/templates-user/my-fantasy-hockey-hub.xml
   ```
3. Navigate to **Docker** -> **Add Container** -> select the **Fantasy-Hockey-Hub** template from the user dropdown.
4. Verify your paths:
   - **Host Port**: `8585` (or your choice)
   - **Appdata Path**: `/mnt/user/appdata/fantasy-hockey` mapped to `/data`
   - **Admin Password**: Choose your secure password
5. Click **Apply**.

---

## 🔑 Yahoo Fantasy API Setup

PuckMetrics can run in **Demo Mode** out of the box with simulated data. To link your live Yahoo Fantasy league:

1. Visit the [Yahoo Developer Network](https://developer.yahoo.com/apps/create/).
2. Create an App with the following settings:
   - **Application Name**: `PuckMetrics`
   - **Application Type**: `Web Application`
   - **Redirect URI**: `http://<YOUR-UNRAID-IP>:8585/auth/yahoo/callback`
   - **API Permissions**: Check **Fantasy Sports** (`fspt-r`).
3. Copy your **Client ID** and **Client Secret**.
4. In PuckMetrics, open the **Settings** tab, enter your credentials, and click **Authorize Yahoo Account**.

---

## 📐 Mathematical Ranking Engine

Yahoo's default rankings often favor big names or preseason draft position. PuckMetrics calculates an objective **Custom Value Score** ($0 - 100$) derived strictly from game statistics:

### 1. Head-to-Head Categories
For each category $c$ active in your league (e.g., G, A, +/-, PIM, PPP, SOG, HIT, BLK, W, GAA, SV%):

$$Z_c = \frac{\text{Stat}_c - \mu_c}{\sigma_c}$$

- Negative categories (e.g., Goals Against Average, Losses) are naturally inverted.
- You can fine-tune multipliers for specific categories (e.g., boosting Hits/Blocks for banger leagues) in the Settings tab.

### 2. Weekly Streaming Rating
Streaming pickups are rated by potential volume:

$$\text{Streaming Rating} = (\text{Games This Week} \times 12) + (\text{Off-Night Games} \times 22)$$

Off-nights (days with 6 or fewer games) receive higher weighting because players are guaranteed to slot into active lineup spots without causing bench conflict.

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|---|---|---|
| `ADMIN_PASSWORD` | Password required to access the dashboard | `admin` |
| `SECRET_KEY` | Secret salt for cookie encryption | `change_me` |
| `DATA_DIR` | Location of SQLite DB and tokens | `/data` |
| `YAHOO_CLIENT_ID` | Yahoo Developer App Client ID | `""` |
| `YAHOO_CLIENT_SECRET` | Yahoo Developer App Client Secret | `""` |
| `YAHOO_REDIRECT_URI` | Yahoo OAuth callback URL | `http://localhost:8585/auth/yahoo/callback` |
| `DEV_MOCK_DATA` | Enable rich demo data if Yahoo is not connected | `true` |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
