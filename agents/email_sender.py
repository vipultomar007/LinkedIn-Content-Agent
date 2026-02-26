"""
Email Sender Agent
Sends beautifully formatted HTML email with all LinkedIn posts ready to copy-paste.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict
from datetime import datetime
from config.settings import Settings

logger = logging.getLogger(__name__)


class EmailSenderAgent:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def send(self, posts: List[Dict]) -> bool:
        subject = f"🚀 Your LinkedIn Posts for {datetime.now().strftime('%b %d, %Y')} ({len(posts)} ready)"
        html_body = self._build_html(posts)
        plain_body = self._build_plain(posts)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.settings.SENDER_EMAIL
        msg["To"] = self.settings.RECIPIENT_EMAIL
        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                server.starttls()
                server.login(self.settings.SENDER_EMAIL, self.settings.SENDER_PASSWORD)
                server.sendmail(
                    self.settings.SENDER_EMAIL,
                    self.settings.RECIPIENT_EMAIL,
                    msg.as_string(),
                )
            logger.info("✅ Email sent successfully!")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False

    def _build_html(self, posts: List[Dict]) -> str:
        category_colors = {
            "AI": "#6366f1",
            "Java": "#f59e0b",
            "LLD": "#10b981",
            "HLD": "#ef4444",
            "Tech": "#3b82f6",
        }

        cards = ""
        for i, post in enumerate(posts, 1):
            color = category_colors.get(post["category"], "#6b7280")
            post_html = post["post"].replace("\n", "<br>")
            cards += f"""
            <div style="background:#fff;border-radius:12px;padding:28px;margin-bottom:24px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.08);border-left:4px solid {color};">
                <div style="display:flex;align-items:center;margin-bottom:16px;">
                    <span style="background:{color};color:#fff;font-size:11px;font-weight:700;
                                 padding:4px 10px;border-radius:20px;letter-spacing:0.5px;">
                        {post['category'].upper()}
                    </span>
                    <span style="margin-left:10px;font-size:11px;color:#9ca3af;">POST {i} of {len(posts)}</span>
                </div>
                <h2 style="margin:0 0 16px;font-size:17px;color:#111827;font-weight:700;">
                    {post['topic']}
                </h2>
                <div style="background:#f9fafb;border-radius:8px;padding:20px;
                            font-size:14px;line-height:1.8;color:#374151;white-space:pre-wrap;">
                    {post_html}
                </div>
                <div style="margin-top:14px;text-align:right;">
                    <span style="font-size:11px;color:#9ca3af;">✅ Copy above and paste to LinkedIn</span>
                </div>
            </div>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                     background:#f3f4f6;margin:0;padding:40px 20px;">
            <div style="max-width:680px;margin:0 auto;">
                <div style="text-align:center;margin-bottom:32px;">
                    <h1 style="font-size:24px;color:#111827;margin:0 0 8px;">
                        🚀 Your LinkedIn Posts Are Ready
                    </h1>
                    <p style="color:#6b7280;font-size:14px;margin:0;">
                        Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} &nbsp;•&nbsp;
                        {len(posts)} posts ready to publish
                    </p>
                </div>
                {cards}
                <div style="text-align:center;margin-top:32px;padding:20px;
                            background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                    <p style="color:#6b7280;font-size:13px;margin:0;">
                        💡 Tip: Post at <strong>8-9 AM</strong> or <strong>12-1 PM</strong> on weekdays for maximum reach.
                        Space posts 1-2 days apart.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _build_plain(self, posts: List[Dict]) -> str:
        lines = [f"Your LinkedIn Posts — {datetime.now().strftime('%B %d, %Y')}\n", "=" * 60]
        for i, post in enumerate(posts, 1):
            lines.append(f"\n--- POST {i}: {post['topic']} [{post['category']}] ---\n")
            lines.append(post["post"])
            lines.append("\n" + "-" * 60)
        lines.append("\nTip: Post at 8-9 AM or 12-1 PM on weekdays for best engagement.")
        return "\n".join(lines)
