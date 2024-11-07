"use client";
import Link from "next/link";

export default function PatientsPage() {
    return (
        <div className="container">
            <h1>Welcome</h1>
            <Link href="/patients/patientList">
                <button className="button">Show Patient List</button>
            </Link>
            <br></br>
            <Link href="/patients/summary">
                <button className="button">Show summary details</button>
            </Link>

            <style jsx>{`
                .container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }

                h1 {
                    font-size: 36px;
                    margin-bottom: 20px;
                }

                .button {
                    padding: 15px 30px;
                    font-size: 20px;
                    background-color: turquoise;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }

                .button:hover {
                    background-color: #008080;
                }
            `}</style>
        </div>
    );
}

