"use client"
import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';


export default function PatientChart() {
  const [labels, setLabels] = useState([]);
  const [values, setValues] = useState([]);

 
  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_data_summary');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const newData = data.map(item => ({
          label: item.day,
          value: item.amount
        }));
        setLabels(newData.map(item => item.label));
        setValues(newData.map(item => item.value));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    fetchData();
  }, []);
  
  useEffect(() => {
    let myChart;
    if (labels.length && values.length) {
       myChart =new Chart(document.getElementById("bar-chart"), { 
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'num patients',
            backgroundColor: [
              '#3e95cd',
              '#8e5ea2',
              '#3cba9f',
              '#e8c3b9',
              '#c45850',
              '#CD5C5C',
              '#40E0D0'
            ],
            data: values
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            title: {
              display: true,
              text: 'corona patients graph'
            },
            legend: {
              display: false
            }
          },
          maintainAspectRatio: false,
          responsive: true,
          aspectRatio: 1.5 
        }
      });
    }
    return ()=>{myChart?.destroy()}
  }, [labels, values]);

  return (
    <canvas id="bar-chart" style={{ width: "800px", height: "650px" }}></canvas>
  );
}
