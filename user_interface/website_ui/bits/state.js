/*
This file contains all the global variables used throughout the application.
 */

// Map.
let map;

// Data.
let DATA = null

// Dropdown menus.
let DATASETS = ["none"]
let COLUMNS = ["blank"]
let SELECTED_DATASET = "none";
let SELECTED_COLUMN = "blank";

// Focused OAs.
let SELECTED_OA = null

// Scale hash maps.
let SCALES_MAP  = new Map()
let SCALES_LABEL_MAP = new Map()

// Map
let MAP_LABELS_ON = false
let HIGH_OPACITY = 0.80
let LOW_OPACITY = 0.30
let OPACITY = HIGH_OPACITY

// Auxiliary visualizations
let LOGARITHMIC_SCALE = false