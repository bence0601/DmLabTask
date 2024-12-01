import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // Import the plugin

// Register the Chart.js components and the plugin
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ChartDataLabels);

const data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr','May' ], // Group labels
  datasets: [
    {
      label: 'Szél (mph)', // First bar in each group
      data: [12, 19, 3, 4, 5], // Adjust data length to match labels
      backgroundColor: 'rgba(75, 192, 192, 0.6)', // greenish
      unit: 'mph', // Add unit for wind speed
    },
    {
      label: 'Hőmérséklet (°C)', // Second bar in each group
      data: [22, 25, 27, 23, 22], // Adjust data length to match labels
      backgroundColor: 'rgba(255, 99, 132, 0.6)', // redish
      unit: '°C', // Add unit for temperature
    },
    {
      label: 'Csapadék (mm)', // Third bar in each group
      data: [50, 45, 30, 4, 3], // Adjust data length to match labels
      backgroundColor: 'rgba(54, 162, 235, 0.6)', // blueish
      unit: 'mm', // Add unit for precipitation
    },
  ],
};

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Időjárás adatok (Több oszlop címkék)',
    },
    datalabels: {
      color: 'black', // Label color
      font: {
        weight: 'bold', // Font weight for the values
        size: 14, // Font size for the values
      },
      align: 'end', // Align labels on top of the bars
      anchor: 'end', // Position the label at the end (top) of each bar
      formatter: (value, context) => {
        const datasetIndex = context.datasetIndex;
        const unit = context.dataset.unit;
        return `${value} ${unit}`;
      },
    },
  },
  scales: {
    x: {
      stacked: false,
      title: {
        display: true,
        text: 'Hónapok',
      },
      ticks: {
        padding: 10, // Adjust spacing between the labels and bars
      },
      // Adjust the category percentage to control the width of the groups
      categoryPercentage: 0.6, // Set a lower value to make bars narrower within each group
    },
    y: {
      stacked: false,
      title: {
        display: true,
        text: 'Értékek',
      },
      beginAtZero: true,
      display: false,
    },
  },
  elements: {
    bar: {
      // Adjust the width of the bars within each category
      barPercentage: 0., // Decrease to make individual bars narrower within their group
    },
  },
};

const TempBarChart = () => {
  return <Bar data={data} options={options} />;
};

export default TempBarChart;
