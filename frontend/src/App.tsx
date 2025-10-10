import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "sonner@2.0.3";
import { QuickExit } from "./components/QuickExit";
import { HomePage } from "./components/HomePage";
import { ReportForm } from "./components/ReportForm";
import { SupportDirectory } from "./components/SupportDirectory";
import { AdminDashboard } from "./components/AdminDashboard";
import { Testimonials } from "./components/Testimonials";

export default function App() {
  return (
    <Router>
      <Toaster position="top-right" richColors />
      <QuickExit />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/report" element={<ReportForm />} />
        <Route path="/support" element={<SupportDirectory />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/testimonials" element={<Testimonials />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
