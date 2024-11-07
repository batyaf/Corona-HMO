"use client"
import Link from 'next/link';
import { useEffect, useState } from 'react';
import NewPatient from './newPatient/page';

export default function PatientsTable() {
    const [patients, setPatients] = useState([]);

    async function getPatientsData() {
        try {
            const response = await fetch("http://localhost:5000/get_all_Patient");
            const patientsJson = await response.json();
            setPatients(patientsJson);
        } catch (error) {
            console.error('Error fetching patients:', error);
        }
    }

    async function deletePatient(id) {
        try {
            await fetch(`http://localhost:5000/delete_patient/${id}`, {
                method: 'DELETE',
            });
            getPatientsData();
        } catch (error) {
            console.error('Error deleting patient:', error);
        }
    }

    useEffect(() => {
        getPatientsData();
    }, []);

    return (
        <>
            <h1>List of Patients</h1>
            <Link href="/patients/patientList/newPatient">
                <button className="actionButton insertButton">Insert New Patient</button>
            </Link>
            <div className="PatientsGrid">
                {patients && patients.map((patient) => (
                    <div key={patient.id} className="PatientCard">
                        <div className="PatientImage">
                           <img 
                              src={`http://127.0.0.1:5000/get_image_by_id/${patient.id}`} 
                              onError={(e) => {
                                e.target.onerror = null; 
                                e.target.src='/images/person.png'; }}
                              alt={`Image of ${patient.firstName} ${patient.lastName}`}
                              className="roundImage"
                          /> 
                        </div>
                        <div className="PatientInfo">
                            <p><span className="label">Id:</span> {patient.id}</p>
                            <p><span className="label">First Name:</span> {patient.firstName}</p>
                            <p><span className="label">Last Name:</span> {patient.lastName}</p>
                            <p><span className="label">Address:</span> {patient.address.street} {patient.address.houseNumber} {patient.address.city.cityName}</p>
                            <p><span className="label">Date of Birth:</span> {patient.dateOfBirth}</p>
                            <p><span className="label">Phone:</span> {patient.phone}</p>
                            <p><span className="label">Mobile Phone:</span> {patient.mobilePhone}</p>
                        </div>
                        <div className="PatientActions">
                            <Link href={`/patients/patientDetails/${patient.id}`}>
                                <button className="actionButton">Show Details</button>
                            </Link>
                            <Link href={`/patients/updatePatient/${patient.id}`}>
                                <button className="actionButton">Update Patient</button>
                            </Link>
                            <button className="actionButton deleteButton" onClick={() => deletePatient(patient.id)}>Delete Patient</button>
                        </div>
                    </div>
                ))}
            </div>
            <br />
            <style jsx>{`
                .PatientsGrid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 20px;
                }

                .PatientCard {
                    border: 1px solid #ccc;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                }

                .label {
                    font-weight: bold;
                }

                .PatientImage {
                    text-align: center;
                }

                .roundImage {
                    border-radius: 50%;
                    max-width: 100%;
                    max-height: 200px;
                    object-fit: cover;
                }

                .emptyImage {
                    background-color: #ccc; /* Placeholder color */
                }

                .PatientInfo {
                    flex: 1;
                }

                .PatientActions {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 10px;
                }

                .actionButton {
                    background-color: #00ced1;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    cursor: pointer;
                    border-radius: 4px;
                    margin:4px;
                }

                .deleteButton {
                    background-color: #ff4500;
                    margin:4px;
                }
            `}</style>
        </>
    );
}
