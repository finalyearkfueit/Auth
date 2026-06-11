"""
Beautiful HTML email templates for AI Studio
"""


class EmailTemplates:
    """Email template generator with professional HTML design."""

    @staticmethod
    def get_otp_email_html(otp_code: str, expiry_minutes: int) -> str:
        """Generate beautiful HTML email for OTP."""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset - AI Studio</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 20px;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 20px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }}
                .header p {{
                    margin: 5px 0 0 0;
                    opacity: 0.9;
                    font-size: 14px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .greeting {{
                    font-size: 16px;
                    color: #333;
                    margin-bottom: 20px;
                }}
                .otp-box {{
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 20px;
                    margin: 30px 0;
                    border-radius: 8px;
                }}
                .otp-label {{
                    font-size: 12px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 10px;
                    font-weight: 600;
                }}
                .otp-code {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #667eea;
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                    text-align: center;
                    margin: 15px 0;
                    word-break: break-all;
                }}
                .expiry-notice {{
                    background: #fff3cd;
                    border: 1px solid #ffc107;
                    border-radius: 6px;
                    padding: 12px 15px;
                    margin: 20px 0;
                    font-size: 13px;
                    color: #856404;
                }}
                .expiry-icon {{
                    margin-right: 8px;
                }}
                .security-note {{
                    background: #e7f3ff;
                    border: 1px solid #b3d9ff;
                    border-radius: 6px;
                    padding: 15px;
                    margin: 20px 0;
                    font-size: 13px;
                    color: #004085;
                    line-height: 1.5;
                }}
                .security-icon {{
                    margin-right: 8px;
                }}
                .instructions {{
                    background: #f0f4f8;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #333;
                }}
                .instructions ol {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .instructions li {{
                    margin: 8px 0;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                .footer-text {{
                    font-size: 12px;
                    color: #666;
                    margin: 8px 0;
                }}
                .footer-logo {{
                    color: #667eea;
                    font-weight: 600;
                    font-size: 14px;
                    margin: 10px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 20px 0;
                }}
                .social-links {{
                    margin-top: 15px;
                }}
                .social-links a {{
                    display: inline-block;
                    margin: 0 10px;
                    color: #667eea;
                    text-decoration: none;
                    font-size: 12px;
                }}
                .divider {{
                    border: none;
                    border-top: 1px solid #e9ecef;
                    margin: 20px 0;
                }}
                @media only screen and (max-width: 600px) {{
                    .container {{
                        border-radius: 0;
                    }}
                    .content {{
                        padding: 25px 15px;
                    }}
                    .otp-code {{
                        font-size: 28px;
                        letter-spacing: 4px;
                    }}
                    .header h1 {{
                        font-size: 22px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Header -->
                <div class="header">
                    <h1>🔐 Password Reset</h1>
                    <p>AI Studio Security</p>
                </div>

                <!-- Content -->
                <div class="content">
                    <div class="greeting">
                        <p>Hello!</p>
                    </div>

                    <p>You've requested to reset your AI Studio password. Use the verification code below to proceed:</p>

                    <!-- OTP Box -->
                    <div class="otp-box">
                        <div class="otp-label">Your Verification Code</div>
                        <div class="otp-code">{otp_code}</div>
                        <p style="text-align: center; color: #666; font-size: 13px; margin: 10px 0;">
                            (Valid for {expiry_minutes} minutes)
                        </p>
                    </div>

                    <!-- Expiry Warning -->
                    <div class="expiry-notice">
                        <span class="expiry-icon">⏱️</span>
                        This code will expire in <strong>{expiry_minutes} minutes</strong>. Please use it promptly.
                    </div>

                    <!-- Instructions -->
                    <div class="instructions">
                        <strong>How to reset your password:</strong>
                        <ol>
                            <li>Copy the verification code above</li>
                            <li>Return to the AI Studio password reset page</li>
                            <li>Paste the code and enter your new password</li>
                            <li>Confirm your new password</li>
                            <li>Click "Reset Password" to complete the process</li>
                        </ol>
                    </div>

                    <!-- Security Note -->
                    <div class="security-note">
                        <span class="security-icon">🔒</span>
                        <strong>Security Tip:</strong> Never share this code with anyone. Our team will never ask for your verification code or password via email.
                    </div>

                    <p style="color: #666; font-size: 14px; margin-top: 20px;">
                        If you didn't request this password reset, please ignore this email or contact our support team immediately.
                    </p>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <div class="footer-logo">🎨 AI Studio</div>
                    <div class="footer-text">Transform Your Images with AI-Powered Tools</div>
                    <div class="divider"></div>
                    <div class="footer-text">© 2024 AI Studio. All rights reserved.</div>
                    <div class="footer-text">
                        Need help? <a href="mailto:support@aistudio.com" style="color: #667eea; text-decoration: none;">Contact Support</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def get_welcome_email_html(username: str) -> str:
        """Generate beautiful HTML welcome email."""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to AI Studio</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 20px;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 20px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 32px;
                    font-weight: 600;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                    font-size: 16px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .greeting {{
                    font-size: 18px;
                    color: #333;
                    margin-bottom: 15px;
                }}
                .features {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 30px 0;
                }}
                .feature {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                    text-align: center;
                }}
                .feature-icon {{
                    font-size: 32px;
                    margin-bottom: 10px;
                }}
                .feature-title {{
                    font-weight: 600;
                    color: #333;
                    margin: 10px 0 5px 0;
                    font-size: 14px;
                }}
                .feature-desc {{
                    color: #666;
                    font-size: 12px;
                    margin: 0;
                }}
                .cta-button {{
                    display: inline-block;
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    text-align: center;
                    margin: 20px 0;
                    box-sizing: border-box;
                }}
                .tips {{
                    background: #e7f3ff;
                    border: 1px solid #b3d9ff;
                    border-radius: 6px;
                    padding: 15px;
                    margin: 20px 0;
                    font-size: 13px;
                    color: #004085;
                }}
                .tips-title {{
                    font-weight: 600;
                    margin-bottom: 8px;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                .footer-text {{
                    font-size: 12px;
                    color: #666;
                    margin: 8px 0;
                }}
                .footer-logo {{
                    color: #667eea;
                    font-weight: 600;
                    font-size: 14px;
                    margin: 10px 0;
                }}
                @media only screen and (max-width: 600px) {{
                    .features {{
                        grid-template-columns: 1fr;
                    }}
                    .container {{
                        border-radius: 0;
                    }}
                    .content {{
                        padding: 25px 15px;
                    }}
                    .header h1 {{
                        font-size: 26px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Header -->
                <div class="header">
                    <h1>🎨 Welcome to AI Studio!</h1>
                    <p>Your account is ready to go</p>
                </div>

                <!-- Content -->
                <div class="content">
                    <div class="greeting">
                        <p>Hey <strong>{username}</strong>,</p>
                    </div>

                    <p>Welcome to AI Studio! We're thrilled to have you on board. Your account has been successfully created and you're ready to start transforming your images with our powerful AI tools.</p>

                    <!-- Features Grid -->
                    <div class="features">
                        <div class="feature">
                            <div class="feature-icon">🔄</div>
                            <div class="feature-title">Background Removal</div>
                            <p class="feature-desc">Remove backgrounds instantly</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">✨</div>
                            <div class="feature-title">Image Enhancement</div>
                            <p class="feature-desc">Enhance quality & clarity</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">👕</div>
                            <div class="feature-title">Cloth Swap</div>
                            <p class="feature-desc">Change clothing virtually</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">⚡</div>
                            <div class="feature-title">AI Powered</div>
                            <p class="feature-desc">Advanced technology</p>
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="http://localhost:3000/login" class="cta-button">Get Started Now</a>

                    <!-- Tips -->
                    <div class="tips">
                        <div class="tips-title">💡 Quick Tips:</div>
                        <ul style="margin: 8px 0; padding-left: 20px;">
                            <li>You can upload images directly from your device</li>
                            <li>Try different tools on the same image</li>
                            <li>Save your favorite results to your library</li>
                            <li>Share your creations with others</li>
                        </ul>
                    </div>

                    <p style="color: #666; font-size: 14px;">
                        If you have any questions or need help, don't hesitate to contact our support team.
                    </p>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <div class="footer-logo">🎨 AI Studio</div>
                    <div class="footer-text">Transform Your Images with AI-Powered Tools</div>
                    <hr style="border: none; border-top: 1px solid #e9ecef; margin: 15px 0;">
                    <div class="footer-text">© 2024 AI Studio. All rights reserved.</div>
                    <div class="footer-text">
                        <a href="http://localhost:3000" style="color: #667eea; text-decoration: none; margin-right: 15px;">Home</a>
                        <a href="mailto:support@aistudio.com" style="color: #667eea; text-decoration: none;">Support</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
