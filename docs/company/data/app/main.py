from fastapi import FastAPI, Request
import os, hashlib, logging, subprocess

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/predict")
async def predict(req: Request):
    body = await req.json()
    # ❌ weak hashing (Bandit will flag)
    uid = hashlib.md5(body.get("user","anon").encode()).hexdigest()
    # ❌ noisy logs (potential info leak)
    logging.info(f"headers={dict(req.headers)} body={body}")
    # ❌ hardcoded-looking secret (Gitleaks will flag even though it's fake)
    payment_api_key = os.getenv("PAYMENT_API_KEY", "sk_test_1234567890ABCDEFGHIJKLMNOP")
    return {"id": uid, "result": "hello"}

@app.get("/shell")  # ❌ command injection vector (Bandit B602/B607)
def shell(cmd: str = "echo hi"):
    return {"out": subprocess.getoutput(cmd)}
