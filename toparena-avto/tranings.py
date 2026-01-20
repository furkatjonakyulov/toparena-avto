import pandas as pd
import logging

# LOG sozlash
logging.basicConfig(
    filename="toparena_schedule.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def automate_schedule(requests_file, schedule_file):
    try:
        logging.info("Rejalashtirish jarayoni boshlandi")

        requests_df = pd.read_excel(requests_file)
        schedule_df = pd.read_excel(schedule_file)

        required_cols = ["date", "time", "team", "type"]
        for col in required_cols:
            if col not in requests_df.columns:
                raise ValueError(f"Majburiy ustun yo‘q: {col}")

        for _, row in requests_df.iterrows():
            conflict = schedule_df[
                (schedule_df["date"] == row["date"]) &
                (schedule_df["time"] == row["time"]) &
                (schedule_df["team"] == row["team"])
            ]

            if not conflict.empty:
                logging.warning(
                    f"To‘qnashuv: {row['team']} - {row['date']} {row['time']}"
                )
                continue

            schedule_df = pd.concat([schedule_df, pd.DataFrame([row])])

            logging.info(
                f"Qo‘shildi: {row['team']} - {row['type']} - {row['date']} {row['time']}"
            )

        schedule_df.to_excel(schedule_file, index=False)
        logging.info("Jarayon muvaffaqiyatli yakunlandi")

    except Exception as e:
        logging.error(f"Kritik xato: {e}")

if __name__ == "__main__":
    automate_schedule(
        requests_file="new_requests.xlsx",
        schedule_file="current_schedule.xlsx"
    )