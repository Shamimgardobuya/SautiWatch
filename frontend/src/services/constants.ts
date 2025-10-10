/**
 * API Constants and Type Definitions
 * Centralized location for all constants used in the application
 */

// Incident Types
export const INCIDENT_TYPES = {
  PHYSICAL: 'physical',
  SEXUAL: 'sexual',
  EMOTIONAL: 'emotional',
  FINANCIAL: 'financial',
  STALKING: 'stalking',
  OTHER: 'other',
} as const;

export const INCIDENT_TYPE_LABELS: Record<string, string> = {
  [INCIDENT_TYPES.PHYSICAL]: 'Physical Violence',
  [INCIDENT_TYPES.SEXUAL]: 'Sexual Violence',
  [INCIDENT_TYPES.EMOTIONAL]: 'Emotional/Psychological Abuse',
  [INCIDENT_TYPES.FINANCIAL]: 'Financial Abuse',
  [INCIDENT_TYPES.STALKING]: 'Stalking/Harassment',
  [INCIDENT_TYPES.OTHER]: 'Other',
};

// Urgency Levels
export const URGENCY_LEVELS = {
  CRITICAL: 'critical',
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low',
} as const;

export const URGENCY_LABELS: Record<string, string> = {
  [URGENCY_LEVELS.CRITICAL]: 'Critical - Immediate danger',
  [URGENCY_LEVELS.HIGH]: 'High - Urgent attention needed',
  [URGENCY_LEVELS.MEDIUM]: 'Medium - Important but not urgent',
  [URGENCY_LEVELS.LOW]: 'Low - For record/pattern tracking',
};

// Report Status
export const REPORT_STATUS = {
  PENDING: 'pending',
  VERIFIED: 'verified',
  INVESTIGATING: 'investigating',
  FLAGGED: 'flagged',
  CLOSED: 'closed',
} as const;

export const STATUS_LABELS: Record<string, string> = {
  [REPORT_STATUS.PENDING]: 'Pending Review',
  [REPORT_STATUS.VERIFIED]: 'Verified',
  [REPORT_STATUS.INVESTIGATING]: 'Under Investigation',
  [REPORT_STATUS.FLAGGED]: 'Flagged',
  [REPORT_STATUS.CLOSED]: 'Closed',
};

// Status Badge Colors (Tailwind classes)
export const STATUS_COLORS: Record<string, string> = {
  [REPORT_STATUS.PENDING]: 'bg-yellow-600',
  [REPORT_STATUS.VERIFIED]: 'bg-green-600',
  [REPORT_STATUS.INVESTIGATING]: 'bg-blue-600',
  [REPORT_STATUS.FLAGGED]: 'bg-red-600',
  [REPORT_STATUS.CLOSED]: 'bg-gray-600',
};

// Urgency Badge Colors (Tailwind classes)
export const URGENCY_COLORS: Record<string, string> = {
  [URGENCY_LEVELS.CRITICAL]: 'bg-red-600',
  [URGENCY_LEVELS.HIGH]: 'bg-orange-600',
  [URGENCY_LEVELS.MEDIUM]: 'bg-yellow-600',
  [URGENCY_LEVELS.LOW]: 'bg-blue-600',
};

// Emergency Contacts
export const EMERGENCY_CONTACTS = {
  POLICE: '999',
  CRISIS_HOTLINE: '+254 700 678 901',
  GBV_HOTLINE: '1195',
  CHILD_HELPLINE: '116',
} as const;

// API Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection and try again.',
  SERVER_ERROR: 'Server error. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  GENERIC: 'An unexpected error occurred. Please try again.',
} as const;

// Form Validation
export const VALIDATION = {
  MIN_DESCRIPTION_LENGTH: 10,
  MAX_DESCRIPTION_LENGTH: 2000,
  MAX_LOCATION_LENGTH: 255,
  MAX_ABUSER_INFO_LENGTH: 500,
} as const;

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM DD, YYYY',
  INPUT: 'YYYY-MM-DD',
  DATETIME: 'MMM DD, YYYY HH:mm',
} as const;

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
} as const;

// Cache TTL (Time To Live) in milliseconds
export const CACHE_TTL = {
  SUPPORT_SERVICES: 5 * 60 * 1000, // 5 minutes
  TESTIMONIALS: 10 * 60 * 1000,    // 10 minutes
  REPORTS: 30 * 1000,               // 30 seconds
} as const;

// Type Guards
export type IncidentType = typeof INCIDENT_TYPES[keyof typeof INCIDENT_TYPES];
export type UrgencyLevel = typeof URGENCY_LEVELS[keyof typeof URGENCY_LEVELS];
export type ReportStatus = typeof REPORT_STATUS[keyof typeof REPORT_STATUS];

export function isValidIncidentType(value: string): value is IncidentType {
  return Object.values(INCIDENT_TYPES).includes(value as IncidentType);
}

export function isValidUrgencyLevel(value: string): value is UrgencyLevel {
  return Object.values(URGENCY_LEVELS).includes(value as UrgencyLevel);
}

export function isValidReportStatus(value: string): value is ReportStatus {
  return Object.values(REPORT_STATUS).includes(value as ReportStatus);
}
