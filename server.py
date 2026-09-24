import os
import psycopg2
import resend
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


load_dotenv()


resend.api_key = os.getenv("RESEND_API_KEY")


mcp = FastMCP("My Onboarding MCP Server")
# TOOL 1: Check CockroachDB Connection
#CockroachDB Connection
@mcp.tool()
def check_database() -> str:

    db_url = os.getenv("COCKROACH_DB_URL")
    if not db_url:
        return "Error: COCKROACH_DB_URL is missing in .env file"
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        conn.close()
        return f"SUCCESS! CockroachDB Connected: {version[0]}"
    except Exception as e:
        return f"Database Error: {str(e)}"

# TOOL 2: Send Email via Resend
@mcp.tool()
def send_email(to_email: str, subject: str, message_body: str) -> str:
   
    try:
        response = resend.Emails.send({
            "from": "vaanya@resend.dev",
            "to": to_email,
            "subject": subject,
            "html": f"<p>{message_body}</p>"
        })
        return f"Email sent! Message ID: {response.get('id')}"
    except Exception as e:
        return f"Email Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()