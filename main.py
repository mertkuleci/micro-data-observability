import json
from ingestion import setup_database
from observability import run_all_checks
from llm_agent import analyze_anomalies
from notifier import send_telegram_alert

def main():
    print("1. Setting up database and generating test data...")
    conn = setup_database()

    print("2. Running data quality and anomaly checks...")
    check_results = run_all_checks(conn)

    anomalies_found = [res for res in check_results if res.get("is_anomaly")]

    if not anomalies_found:
        print("All checks passed! No anomalies detected.")
        return

    print(f"\n⚠️ {len(anomalies_found)} anomaly/anomalies detected!")
    anomalies_json = json.dumps(anomalies_found, indent=2, ensure_ascii=False)
    print(anomalies_json)

    print("\n3. Generating root cause analysis with LLM Agent...")
    llm_analysis = analyze_anomalies(anomalies_json)
    print("\n--- AI Root Cause Analysis Result ---")
    print(llm_analysis)

    print("\n4. Sending Telegram alert...")
    alert_message = (
        f"🚨 DATA ANOMALY ALERT 🚨\n\n"
        f"Detected Anomalies:\n{anomalies_json}\n\n"
        f"AI Root Cause & Fix Recommendation:\n{llm_analysis}"
    )

    send_telegram_alert(alert_message)

if __name__ == "__main__":
    main()