from dotenv import load_dotenv
from flask import request, jsonify, url_for

# from .app import app
from app import app as appRouter

load_dotenv()

providers = ["google", "github", "microsoft", "wc", "ibm"]


# OAuth callback route for Google, Microsoft, GitHub, etc.
@appRouter.route("/login/<provider>")
def login(provider):
    from oauth import OAuthIntegration
    if provider not in providers:
        return jsonify({"error": "Invalid provider"}), 400

    oauth_integration = OAuthIntegration(provider)
    oauth_session = oauth_integration.get_oauth_session(appRouter)
    return oauth_session.authorize(callback=url_for('authorized', provider=provider, _external=True))


@appRouter.route("/callback/<provider>")
def authorized(provider):
    from oauth import OAuthIntegration
    if provider not in providers:
        return jsonify({"error": "Invalid provider"}), 400

    oauth_integration = OAuthIntegration(provider)
    try:
        oauth_token = oauth_integration.get_oauth_token(appRouter, request.args)
    except Exception as e:
        return jsonify({"error": f"OAuth authentication failed: {str(e)}"}), 400

    return jsonify({
        "access_token": oauth_token.access_token,
        "token_type": oauth_token.token_type,
        "expires_in": oauth_token.expires_in
    })


# Example route for getting user info (expand as needed)
@appRouter.route("/user/<provider>")
def user_info(provider):
    from oauth import OAuthIntegration
    token = request.args.get("access_token")
    if not token:
        return jsonify({"error": "Access token is required"}), 400

    if provider not in providers:
        return jsonify({"error": "Invalid provider"}), 400

    oauth_integration = OAuthIntegration(provider)
    oauth_session = oauth_integration.get_oauth_session(appRouter)

    # Set the tokengetter to properly fetch the access token
    oauth_session.tokengetter(lambda: {"access_token": token})

    # Request user info from the provider
    user_info_response = oauth_session.get(oauth_integration.get_user_info_url(provider))

    # Check if the response is successful
    if user_info_response.status != 200:
        return jsonify({"error": "Failed to fetch user info"}), 400
    return jsonify(user_info_response.data)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
