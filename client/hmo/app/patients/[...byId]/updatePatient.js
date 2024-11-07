"use client";
import { useState, useEffect } from 'react';

export default function UpdatePatient(props) {
    const { id } = props;
    const [patient, setPatient] = useState(null);
    const [cities, setCtieis] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
  

    async function getPatientData() {
        const response = await fetch(`http://127.0.0.1:5000/get_patient_by_id/${id}`);
        const patientJson = await response.json();
        setPatient(patientJson);
    }

    async function getCitiesData() {
        const response = await fetch(`http://127.0.0.1:5000/get_all_cities`);
        const citiesJson = await response.json();
        setCtieis(citiesJson);
    }

    useEffect(() => {
        getPatientData();
        getCitiesData();
    }, []);

    function changeDetail(e) {
        const { name, value } = e.target;
        setPatient(prevPatient => ({
            ...prevPatient,
            [name]: value
        }));
    };

    function selectedCity(e) {
        const { value } = e.target;
        const selectedCity = cities.find(city => city.cityName === value);
        if (selectedCity) {
            setPatient(prevPatient => ({
                ...prevPatient,
                address: {
                    ...prevPatient.address,
                    city: {
                        cityName: selectedCity.cityName,
                        cityCode: selectedCity.cityCode
                    }
                }
            }));
        }
    }


    function handleAddressChange(e) {
        const { name, value } = e.target;
        const [parent, field] = name.split('.');
        setPatient(prevPatient => ({
            ...prevPatient,
            address: {
                ...prevPatient.address,
                [field]: value
            }
        }));
    }



    async function updatePatient() {
        let errorMessage = '';

        // Check for missing fields
        if (!patient.firstName) {
            errorMessage += 'First name is required.\n';
        }
        if (!patient.lastName) {
            errorMessage += 'Last name is required.\n';
        }
        if (!patient.address.street) {
            errorMessage += 'Street address is required.\n';
        }
        if (!patient.address.houseNumber) {
            errorMessage += 'House number is required.\n';
        }
        if (!patient.address.city.cityName) {
            errorMessage += 'City name is required.\n';
        }
        if (!patient.dateOfBirth) {
            errorMessage += 'Date of birth is required.\n';
        }
        if (!patient.phone) {
            errorMessage += 'Phone number is required.\n';
        }
        if (!patient.mobilePhone) {
            errorMessage += 'Mobile phone number is required.\n';
        }

        // Update the state with the error message
        setErrorMessage(errorMessage);

        // If all integrity checks pass, proceed with the update
        if (!errorMessage) {
            try {
                const response = await fetch(`http://localhost:5000/update_patient`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(patient),
                });
                const json= await response.json();
                if (response.ok) {
                    setErrorMessage('Patient updated successfully');
                } else {
                    setErrorMessage(json.error);
                }
            } catch (error) {
                console.error('Error updating patient:', error);
                setErrorMessage('Error updating patient');
            }
        }
    }

    return (
        <>
            <h1>Update Patient Details</h1>
            <h2>ID: {id}</h2>
            {patient && (
                <div className="updatePatientForm">
                    <div className="formGroup">
                        <label htmlFor="firstName">First Name:</label>
                        <input type="text" id="firstName" name="firstName" value={patient.firstName} onChange={changeDetail} />
                    </div>
                    <div className="formGroup">
                        <label htmlFor="lastName">Last Name:</label>
                        <input type="text" id="lastName" name="lastName" value={patient.lastName} onChange={changeDetail} />
                    </div>
                    <div className="formGroup">
                        <label htmlFor="street">Street:</label>
                        <input type="text" id="street" name="address.street" value={patient.address.street} onChange={handleAddressChange} />
                    </div>
                    <div className="formGroup">
                        <label htmlFor="houseNumber">House Number:</label>
                        <input type="number" id="houseNumber" name="address.houseNumber" value={patient.address.houseNumber} onChange={handleAddressChange} />
                    </div>
                    <div className="formGroup">
                        <label htmlFor="city">City:</label>
                        <select id="city" name="address.city.cityName" value={patient.address.city.cityName} onChange={selectedCity}>
                            {cities && cities.map(city => (
                                <option key={city.cityCode} value={city.cityName}>{city.cityName}</option>
                            ))}
                        </select>
                    </div>
                    <div className="formGroup">
                        <label htmlFor="dateOfBirth">Date of Birth:</label>
                        <input type="date" id="dateOfBirth" name="dateOfBirth" value={patient.dateOfBirth} onChange={changeDetail} />
                    </div>
                    <div className="formGroup">
                        <label htmlFor="phone">Phone:</label>
                        <input type="number" id="phone" name="phone" value={patient.phone} onChange={changeDetail} />
                    </div>
                    <div className="formGroup">
                        <label htmlFor="mobilePhone">Mobile Phone:</label>
                        <input type="number" id="mobilePhone" name="mobilePhone" value={patient.mobilePhone} onChange={changeDetail} />
                    </div>
                    <div className="formGroup">
                        <button onClick={updatePatient}>Update</button>
                    </div>
                    {errorMessage && <div className="error-message">{errorMessage}</div>}
                   </div>
            )}
            <style jsx>{`

                h1 {
                    margin-bottom: 20px;
                    color: turquoise;
                }
                .updatePatientForm {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                }

                .formGroup {
                    display: flex;
                    flex-direction: column;
                }

                label {
                    font-weight: bold;
                }

                input, select {
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }

                button {
                    padding: 8px 16px;
                    background-color: turquoise;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    justify-self: center; /* Centers the button horizontally */
                }

                .error-message {
                    color: red;
                }
            `}</style>
        </>
    );
}


















