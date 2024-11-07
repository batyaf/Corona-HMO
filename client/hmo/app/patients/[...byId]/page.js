"use client";
import { useParams } from "next/navigation";
import PatientDetails from "./patientDetails";
import UpdatePatient from "./updatePatient";

export default function ById() {
   const {byId}=useParams()
    return (
        <>{byId[0]==='patientDetails'&&
           <PatientDetails id={byId[1]}></PatientDetails>
           }
           {byId[0]==='updatePatient'&&
           <UpdatePatient id={byId[1]}></UpdatePatient>
           }


        </>
    );
}