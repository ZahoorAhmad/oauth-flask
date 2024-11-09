import os
from flask import Flask, request, jsonify, url_for
from oauth import OAuthIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# OAuth callback route for Google, Microsoft, GitHub, etc.
@app.route("/login/<provider>")
def login(provider):
    if provider not in ["google", "github", "microsoft"]:
        return jsonify({"error": "Invalid provider"}), 400

    oauth_integration = OAuthIntegration(provider)
    oauth_session = oauth_integration.get_oauth_session(app)
    return oauth_session.authorize(callback=url_for('authorized', provider=provider, _external=True))

@app.route("/callback/<provider>")
def authorized(provider):
    if provider not in ["google", "github", "microsoft"]:
        return jsonify({"error": "Invalid provider"}), 400

    oauth_integration = OAuthIntegration(provider)
    try:
        oauth_token = oauth_integration.get_oauth_token(app, request.args)
    except Exception as e:
        return jsonify({"error": f"OAuth authentication failed: {str(e)}"}), 400

    return jsonify({
        "access_token": oauth_token.access_token,
        "token_type": oauth_token.token_type,
        "expires_in": oauth_token.expires_in
    })

# Example route for getting user info (expand as needed)
@app.route("/user/<provider>")
def user_info(provider):
    token = request.args.get("access_token")
    if not token:
        return jsonify({"error": "Access token is required"}), 400

    if provider not in ['google', 'github', 'microsoft']:
        return jsonify({"error": "Invalid provider"}), 400

    oauth_integration = OAuthIntegration(provider)
    oauth_session = oauth_integration.get_oauth_session(app)
    oauth_session.token = {"access_token": token}

    # Fetch user info based on the provider
    if provider == "google":
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    elif provider == "github":
        user_info_url = "https://api.github.com/user"
    elif provider == "microsoft":
        user_info_url = "https://graph.microsoft.com/v1.0/me"

    user_info_response = oauth_session.get(user_info_url)
    if user_info_response.status_code != 200:
        return jsonify({"error": "Failed to fetch user info"}), 400

    return jsonify(user_info_response.json())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
