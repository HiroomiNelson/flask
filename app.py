from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

def get_x_signature_exchange_poin(
    package_code: str,
    token_confirmation: str,
    path: str,
    method: str,
    timestamp: int,
) -> str:
    hash_str = "ae-hei_9Tee6he+Ik3Gais5="
    hmac_sha512_key = "J1WaShQPHJ1QCK0L77HvuZRaP4XkZ7uiutvazkKPMC7cUP0rz28X8r5Cicnh7BZharamWxDt9nRG5DbjvuF7wG53TeJaPFwNzExCJCuAcEmA8h2tX5XgY43203fHSux6"
    key = f"{hmac_sha512_key};{timestamp}#{hash_str};{method};{path};{timestamp}"
    msg = f"{token_confirmation};{timestamp};{package_code};"

    signature = hmac.new(
        key.encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()
    return signature

@app.route("/get-signature-point", methods=["POST"])
def api_get_signature():
    try:
        data = request.get_json(force=True)
        signature = get_x_signature_exchange_poin(
            package_code=data["package_code"],
            token_confirmation=data["token_confirmation"],
            path=data["path"],
            method=data["method"],
            timestamp=int(data["timestamp"])
        )
        return jsonify({"signature": signature}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
