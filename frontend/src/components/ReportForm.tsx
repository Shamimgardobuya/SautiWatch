import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AlertCircle, CheckCircle, XCircle } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Alert, AlertDescription } from "./ui/alert";
import { reportAPI, type ApiError, API_BASE_URL } from "../services/api";

export function ReportForm() {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [regions, setRegions] = useState<{ id: number; name: string }[]>([]);
  const [formData, setFormData] = useState({
    incidentType: "",
    location: "",
    urgency: "",
    date: "",
    description: "",
    abuserInfo: "",
    region: "",
    image: null as File | null,
  });

  // Fetch regions for the dropdown
 useEffect(() => {
  async function fetchRegions() {
    try {
      const res = await fetch(`${API_BASE_URL}/regions/`);
      const data = await res.json();
      console.log("Regions fetched:", data); // 🔹 add this to debug
      setRegions(data);
    } catch (err) {
      console.error("Error fetching regions:", err);
    }
  }
  fetchRegions();
}, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const payload = new FormData();
      payload.append("victim_name", ""); // Anonymous
      payload.append("is_anonymous", "true");
      payload.append("assaulter_name", formData.abuserInfo || "");
      payload.append("location", formData.location);
      payload.append("urgency_level", formData.urgency);
      payload.append("incident_date", formData.date);
      payload.append("incident_description", formData.description || "");
      if (formData.region) payload.append("region", formData.region);
      if (formData.image) payload.append("image", formData.image);

      const response = await fetch(`${API_BASE_URL}/reports/`, {
        method: "POST",
        body: payload,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw {
          message: errData.message || `Error submitting report: ${response.status}`,
          status: response.status,
        } as ApiError;
      }

      setIsSubmitting(false);
      setShowSuccess(true);

      setTimeout(() => {
        navigate("/support");
      }, 3000);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || "Failed to submit report. Please try again.");
      setIsSubmitting(false);
    }
  };

  if (showSuccess) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <div className="flex items-center gap-2 text-green-600 mb-2">
              <CheckCircle className="h-8 w-8" />
              <CardTitle>Report Submitted Successfully</CardTitle>
            </div>
            <CardDescription>
              Your report has been received and is being processed. You will be connected to support services.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                A case officer will review your report. If verified, it will be forwarded to the appropriate authorities.
              </p>
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm">
                  You are being redirected to our support network directory where you can find immediate help...
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 py-12 px-4">
      <div className="container mx-auto max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle>Anonymous Case Report</CardTitle>
            <CardDescription>
              Your identity is completely protected. All information is encrypted and handled with care.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Alert className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                If you are in immediate danger, please call emergency services or your local police.
              </AlertDescription>
            </Alert>

            {error && (
              <Alert variant="destructive" className="mb-6">
                <XCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Incident Type */}
              <div className="space-y-2">
                <Label htmlFor="incidentType">Type of Incident</Label>
                <Select
                  required
                  onValueChange={(value) => setFormData({ ...formData, incidentType: value })}
                >
                  <SelectTrigger id="incidentType">
                    <SelectValue placeholder="Select incident type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="physical">Physical Violence</SelectItem>
                    <SelectItem value="sexual">Sexual Violence</SelectItem>
                    <SelectItem value="emotional">Emotional/Psychological Abuse</SelectItem>
                    <SelectItem value="financial">Financial Abuse</SelectItem>
                    <SelectItem value="stalking">Stalking/Harassment</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Region */}
              <div className="space-y-2">
                <Label htmlFor="region">Region</Label>
                <Select
                  required
                  onValueChange={(value) => setFormData({ ...formData, region: value })}
                >
                  <SelectTrigger id="region">
                    <SelectValue placeholder="Select your region" />
                  </SelectTrigger>
                  <SelectContent>
                    {regions.map((r) => (
                      <SelectItem key={r.id} value={r.id.toString()}>
                        {r.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Location */}
              <div className="space-y-2">
                <Label htmlFor="location">Location (Area/District)</Label>
                <Input
                  id="location"
                  required
                  placeholder="e.g., Nairobi, Kibera"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                />
                <p className="text-xs text-muted-foreground">
                  General area only - do not provide exact address unless you feel safe doing so
                </p>
              </div>

              {/* Urgency */}
              <div className="space-y-2">
                <Label htmlFor="urgency">Urgency Level</Label>
                <Select
                  required
                  onValueChange={(value) => setFormData({ ...formData, urgency: value })}
                >
                  <SelectTrigger id="urgency">
                    <SelectValue placeholder="Select urgency level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="critical">Critical - Immediate danger</SelectItem>
                    <SelectItem value="high">High - Urgent attention needed</SelectItem>
                    <SelectItem value="medium">Medium - Important but not urgent</SelectItem>
                    <SelectItem value="low">Low - For record/pattern tracking</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Incident Date */}
              <div className="space-y-2">
                <Label htmlFor="date">Date of Incident</Label>
                <Input
                  id="date"
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  max={new Date().toISOString().split("T")[0]}
                />
              </div>

              {/* Abuser Info */}
              <div className="space-y-2">
                <Label htmlFor="abuserInfo">Abuser Information (Optional)</Label>
                <Input
                  id="abuserInfo"
                  placeholder="Name, relationship, or any identifying information"
                  value={formData.abuserInfo}
                  onChange={(e) => setFormData({ ...formData, abuserInfo: e.target.value })}
                />
                <p className="text-xs text-muted-foreground">
                  Only share what you feel comfortable sharing
                </p>
              </div>

              {/* Incident Description */}
              <div className="space-y-2">
                <Label htmlFor="description">Description of Incident (Optional)</Label>
                <Textarea
                  id="description"
                  placeholder="Please describe what happened. Share as much or as little as you're comfortable with."
                  rows={6}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              {/* Image Upload */}
              <div className="space-y-2">
                <Label htmlFor="image">Upload Image (Optional)</Label>
                <Input
                  id="image"
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      setFormData({ ...formData, image: e.target.files[0] });
                    }
                  }}
                />
              </div>

              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-sm text-green-800">
                  <strong>What happens next:</strong> Your report will be reviewed by trained case officers. 
                  If verified, it will be forwarded to relevant authorities. You'll also get immediate access 
                  to support services.
                </p>
              </div>

              {/* Buttons */}
              <div className="flex gap-4">
                <Button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Submitting Securely..." : "Submit Report"}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate("/")}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
