/**
 * UI-related functionality for the POSCAR/CIF converter application
 */

import { state } from './main.js';
import { 
  handleFileUpload, 
  downloadFile, 
  downloadAll, 
  removeFile
} from './fileHandler.js';
import { 
  convertFile, 
  convertAllToCIF, 
  convertAllToPOSCAR,
  convertTextToCIF,
  convertTextToPOSCAR,
  downloadOutputText
} from './converter.js';

/**
 * Initialize UI components
 */
export function initUI() {
  // Set up tab functionality
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      switchTab(tab.dataset.tab, tab);
    });
  });
}

/**
 * Switch between tabs
 * @param {string} tabId - ID of the tab content to show
 * @param {HTMLElement} tabButton - The tab button that was clicked
 */
function switchTab(tabId, tabButton) {
  // Hide all tab contents
  document.querySelectorAll('.tab-content').forEach(tab => {
    tab.classList.add('hidden');
    tab.classList.remove('active');
  });
  
  // Deactivate all tabs
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.remove('active');
    tab.classList.remove('text-blue-600', 'border-b-2', 'border-blue-500', 'font-medium');
    tab.classList.add('text-gray-600');
  });
  
  // Activate selected tab and content
  document.getElementById(tabId).classList.remove('hidden');
  document.getElementById(tabId).classList.add('active');
  
  tabButton.classList.add('active', 'text-blue-600', 'border-b-2', 'border-blue-500', 'font-medium');
  tabButton.classList.remove('text-gray-600');
}

/**
 * Update file list UI
 */
export function updateFileList() {
  const fileListElement = document.getElementById('fileList');
  fileListElement.innerHTML = '';
  
  Object.keys(state.files).forEach(fileId => {
    const file = state.files[fileId];
    const fileElement = document.createElement('div');
    fileElement.className = 'flex justify-between items-center p-3 border border-gray-200 rounded-md bg-gray-50';
    
    const fileNameDiv = document.createElement('div');
    fileNameDiv.className = 'flex-grow mr-4 text-gray-700';
    fileNameDiv.textContent = `${file.name} (${file.description})`;
    
    const fileActions = document.createElement('div');
    fileActions.className = 'flex gap-2';
    
    // Convert button
    const convertButton = document.createElement('button');
    if (file.type === 'poscar') {
      convertButton.textContent = 'Convert to CIF';
      convertButton.onclick = () => convertFile(fileId, 'to-cif');
    } else {
      convertButton.textContent = 'Convert to POSCAR';
      convertButton.onclick = () => convertFile(fileId, 'to-poscar');
    }
    convertButton.className = 'bg-amber-500 hover:bg-amber-600 text-white py-1 px-3 rounded-md text-sm transition';
    
    // Download button
    const downloadButton = document.createElement('button');
    downloadButton.textContent = 'Download';
    downloadButton.onclick = () => downloadFile(fileId);
    downloadButton.className = 'bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded-md text-sm transition';
    
    // Remove button
    const removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.onclick = () => removeFile(fileId);
    removeButton.className = 'bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded-md text-sm transition';
    
    fileActions.appendChild(convertButton);
    fileActions.appendChild(downloadButton);
    fileActions.appendChild(removeButton);
    
    fileElement.appendChild(fileNameDiv);
    fileElement.appendChild(fileActions);
    
    fileListElement.appendChild(fileElement);
  });
}

/**
 * Set up all event listeners
 */
export function setupEventListeners() {
  // File upload tab
  document.getElementById('fileUpload').addEventListener('change', handleFileUpload);
  document.getElementById('convertAllToCIF').addEventListener('click', convertAllToCIF);
  document.getElementById('convertAllToPOSCAR').addEventListener('click', convertAllToPOSCAR);
  document.getElementById('downloadAll').addEventListener('click', downloadAll);
  
  // Text input tab
  document.getElementById('convertToCIF').addEventListener('click', convertTextToCIF);
  document.getElementById('convertToPOSCAR').addEventListener('click', convertTextToPOSCAR);
  document.getElementById('downloadText').addEventListener('click', downloadOutputText);
}
