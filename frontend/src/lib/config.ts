export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export const GITHUB_URL =
  process.env.NEXT_PUBLIC_GITHUB_URL ||
  "https://github.com/student-apis/Student_APIs";

export const SITE_NAME = "Student APIs";
export const SITE_TAGLINE = "Open-source APIs for student developers.";
