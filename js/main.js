/**
 * Main entry point for the POSCAR/CIF converter application
 */

import { initUI, setupEventListeners } from './ui.js';
import { initConverter } from './converter.js';

// Global state accessible to all modules
export const state = {
  pyodideReady: null,
  pyodideInstance: null,
  files: {},
  fileCounter: 0
};

// Initialize the application
async function initApp() {
  // Initialize UI components
  initUI();
  
  try {
    // Initialize Python converter
    state.pyodideReady = initConverter();
    
    // Set up event listeners for all buttons and tabs
    setupEventListeners();
    
  } catch (error) {
    console.error('Application initialization error:', error);
    document.getElementById('status').textContent = 'Initialization failed: ' + error.message;
  }
}

// Start the application when DOM is fully loaded
document.addEventListener('DOMContentLoaded', initApp);
