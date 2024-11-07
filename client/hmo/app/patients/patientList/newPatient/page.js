"use client";
import { useRouter } from 'next/navigation';
import { useState, useEffect} from 'react';

export default function NewPatient() {
    const [patient, setPatient] = useState({
        id:'',
        firstName: '',
        lastName: '',
        address: {
            addressCode:' ',
            street: '',
            houseNumber: '',
            city: {
                cityName: '',
                cityCode: ''
            }
        },
        dateOfBirth: '',
        phone: '',
        mobilePhone: ''
    });
    const [cities,setCities]=useState(null)
    const [errorMessage, setErrorMessage] = useState('');
    const [image, setImage] = useState(null); 
    const router=useRouter();

    async function getCitiesData() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/get_all_cities`);
            const citiesJson = await response.json();
            setCities(citiesJson);
        } catch (error) {
            console.error('Error fetching cities:', error);
        }
    }

    useEffect(() => {
        getCitiesData();
    }, []);

    function handleChange(e) {
        const { name, value } = e.target;
        setPatient(prevPatient => ({
            ...prevPatient,
            [name]: value
        }));
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

    const changeHandler = (e) => {
        setImage(e.target.files[0]);
    };
  
    const insertPatient = async () => {
        let errorMessage = '';
    
        if (!patient.id) {
            errorMessage += 'id is required.\n';
        }
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
    
        if (!errorMessage) {
            try {
                const patientResponse = await fetch('http://localhost:5000/insert_patient', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(patient),
                });
    
                if (patientResponse.ok) {
                    setErrorMessage('Patient inserted successfully');
    
                    const formData = new FormData();
                    formData.append("file", image);
                    formData.append("id", patient.id);
    
                    const imageResponse = await fetch("http://127.0.0.1:5000/insert_image", {
                        method: "POST",
                        body: formData
                    });
    
                    if (!imageResponse.ok) {
                        console.log('Error uploading image');
                    }
                    router.push(`/patients/patientDetails/${patient.id}`)
                } else {
                    const errorMessageJson = await patientResponse.json();
                    setErrorMessage(errorMessageJson.error);
                }
            } catch (error) {
                console.error('Error inserting patient:', error);
            }
        }
    };

    return (
        <>
            <h1>Insert Patient</h1>
            <div className="insertPatientForm">
                <div className="formGrop">
                    <label htmlFor="id">ID:</label>
                    <input type="text" id="id" name="id"  value={patient.id} onChange={handleChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="firstName">First Name:</label>
                    <input type="text" id="firstName" name="firstName" value={patient.firstName} onChange={handleChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="lastName">Last Name:</label>
                    <input type="text" id="lastName" name="lastName" value={patient.lastName} onChange={handleChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="address.street">Street:</label>
                    <input type="text" id="address.street" name="address.street" value={patient.address.street} onChange={handleAddressChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="address.houseNumber">House Number:</label>
                    <input type="number" id="address.houseNumber" name="address.houseNumber" value={patient.address.houseNumber} onChange={handleAddressChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="address.city.cityName">City:</label>
                    <select id="address.city.cityName" name="address.city.cityName" value={patient.address.city.cityName} onChange={selectedCity}>
                        <option value="">Select City</option>
                        {cities && cities.map(city => (
                            <option key={city.cityCode} value={city.cityName}>{city.cityName}</option>
                        ))}
                    </select>
                </div>
                <div className="formGrop">
                    <label htmlFor="dateOfBirth">Date of Birth:</label>
                    <input type="date" id="dateOfBirth" name="dateOfBirth" value={patient.dateOfBirth} onChange={handleChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="phone">Phone:</label>
                    <input type="text" id="phone" name="phone" value={patient.phone} onChange={handleChange} />
                </div>
                <div className="formGrop">
                    <label htmlFor="mobilePhone">Mobile Phone:</label>
                    <input type="text" id="mobilePhone" name="mobilePhone" value={patient.mobilePhone} onChange={handleChange} />
                </div>
                <form >
          <input type="file" name="image"  onChange={changeHandler} />
          </form>
                <div className="formGrop">
                    <button className="submitButton" onClick={insertPatient}>Insert</button>
                </div>
            </div>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <style jsx>{`
               h1 {
                margin-bottom: 20px;
                color: turquoise;
            }
            .insertPatientForm {
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













