import { useState, useEffect } from "react";
import { Shield, AlertCircle, CheckCircle, Clock, Filter, XCircle } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Alert, AlertDescription } from "./ui/alert";
import { Textarea } from "./ui/textarea";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Skeleton } from "./ui/skeleton";
import { reportAPI, type Report, type ApiError } from "../services/api";
import { toast } from "sonner@2.0.3";

export function AdminDashboard() {
  const [reports, setReports] = useState<Report[]>([]);
  const [filterStatus, setFilterStatus] = useState("all");
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await reportAPI.list();
      setReports(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || "Failed to load reports. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const updateReportStatus = async (reportId: string, newStatus: string) => {
    try {
      setUpdating(true);
      const updatedReport = await reportAPI.updateStatus(reportId, newStatus, notes);
      
      // Update local state
      setReports(reports.map(report => 
        report.id === reportId ? updatedReport : report
      ));
      
      setNotes("");
      setSelectedReport(null);
      toast.success("Report status updated successfully");
    } catch (err) {
      const apiError = err as ApiError;
      toast.error(apiError.message || "Failed to update report status");
    } finally {
      setUpdating(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const statusConfig: Record<string, { label: string; className: string }> = {
      pending: { label: "Pending Review", className: "bg-yellow-600" },
      verified: { label: "Verified", className: "bg-green-600" },
      investigating: { label: "Under Investigation", className: "bg-blue-600" },
      closed: { label: "Closed", className: "bg-gray-600" },
      flagged: { label: "Flagged", className: "bg-red-600" },
    };
    const config = statusConfig[status] || statusConfig.pending;
    return <Badge className={config.className}>{config.label}</Badge>;
  };

  const getUrgencyBadge = (urgency: string) => {
    const urgencyConfig: Record<string, string> = {
      critical: "bg-red-600",
      high: "bg-orange-600",
      medium: "bg-yellow-600",
      low: "bg-blue-600",
    };
    const className = urgencyConfig[urgency] || "bg-gray-600";
    return <Badge className={className}>{urgency.toUpperCase()}</Badge>;
  };

  const filteredReports = filterStatus === "all" 
    ? reports 
    : reports.filter(r => r.status === filterStatus);

  const stats = {
    total: reports.length,
    pending: reports.filter(r => r.status === 'pending').length,
    verified: reports.filter(r => r.status === 'verified').length,
    critical: reports.filter(r => r.urgency === 'critical').length,
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 py-12 px-4">
      <div className="container mx-auto max-w-7xl">
        <div className="flex items-center gap-3 mb-8">
          <Shield className="h-10 w-10 text-blue-600" />
          <div>
            <h1>Authority Dashboard</h1>
            <p className="text-muted-foreground">Review and manage case reports</p>
          </div>
        </div>

        {/* Error State */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <XCircle className="h-4 w-4" />
            <AlertDescription>
              {error}
              <Button 
                variant="outline" 
                size="sm" 
                className="ml-4"
                onClick={loadReports}
              >
                Try Again
              </Button>
            </AlertDescription>
          </Alert>
        )}

        {/* Loading State */}
        {loading && (
          <>
            <div className="grid md:grid-cols-4 gap-4 mb-8">
              {[1, 2, 3, 4].map((i) => (
                <Card key={i}>
                  <CardHeader className="pb-3">
                    <Skeleton className="h-4 w-24" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-8 w-16" />
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <Card key={i}>
                  <CardHeader>
                    <Skeleton className="h-6 w-3/4" />
                    <Skeleton className="h-4 w-1/2 mt-2" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-20 w-full" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </>
        )}

        {/* Stats */}
        {!loading && !error && (
          <>
            <div className="grid md:grid-cols-4 gap-4 mb-8">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">Total Reports</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl">{stats.total}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">Pending Review</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl text-yellow-600">{stats.pending}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">Verified Cases</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl text-green-600">{stats.verified}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">Critical</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl text-red-600">{stats.critical}</div>
                </CardContent>
              </Card>
            </div>

            {/* Filter */}
            <div className="mb-6 flex items-center gap-4">
              <Filter className="h-5 w-5 text-muted-foreground" />
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Reports</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="verified">Verified</SelectItem>
                  <SelectItem value="investigating">Investigating</SelectItem>
                  <SelectItem value="flagged">Flagged</SelectItem>
                  <SelectItem value="closed">Closed</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Reports List */}
            {filteredReports.length === 0 ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <p className="text-muted-foreground">No reports found.</p>
                </CardContent>
              </Card>
        ) : (
          <div className="space-y-4">
            {filteredReports.map((report) => (
              <Card key={report.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <CardTitle className="text-lg">
                          {report.incidentType.charAt(0).toUpperCase() + report.incidentType.slice(1)} Violence
                        </CardTitle>
                        {getUrgencyBadge(report.urgency)}
                        {getStatusBadge(report.status)}
                      </div>
                      <CardDescription>
                        Reported on {new Date(report.submittedAt).toLocaleDateString()} • 
                        Location: {report.location} • 
                        Incident Date: {new Date(report.date).toLocaleDateString()}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {report.description && (
                      <div>
                        <p className="text-sm mb-1">Description:</p>
                        <p className="text-sm text-muted-foreground bg-gray-50 p-3 rounded">
                          {report.description}
                        </p>
                      </div>
                    )}

                    {report.abuserInfo && (
                      <div>
                        <p className="text-sm mb-1">Abuser Information:</p>
                        <p className="text-sm text-muted-foreground bg-gray-50 p-3 rounded">
                          {report.abuserInfo}
                        </p>
                      </div>
                    )}

                    {report.notes && (
                      <div>
                        <p className="text-sm mb-1">Case Notes:</p>
                        <p className="text-sm text-muted-foreground bg-blue-50 p-3 rounded">
                          {report.notes}
                        </p>
                      </div>
                    )}

                    <div className="flex gap-2 pt-4 border-t">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => setSelectedReport(report)}
                          >
                            <Clock className="h-4 w-4 mr-2" />
                            Update Status
                          </Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Update Case Status</DialogTitle>
                            <DialogDescription>
                              Review and update the status of this case report.
                            </DialogDescription>
                          </DialogHeader>
                          <div className="space-y-4 mt-4">
                            <div>
                              <label className="text-sm mb-2 block">Add Case Notes:</label>
                              <Textarea
                                placeholder="Add any notes about this case..."
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                rows={4}
                              />
                            </div>
                            <div className="flex gap-2 flex-wrap">
                              <Button 
                                size="sm"
                                className="bg-green-600 hover:bg-green-700"
                                onClick={() => updateReportStatus(report.id, 'verified')}
                                disabled={updating}
                              >
                                <CheckCircle className="h-4 w-4 mr-2" />
                                {updating ? "Updating..." : "Mark Verified"}
                              </Button>
                              <Button 
                                size="sm"
                                variant="outline"
                                onClick={() => updateReportStatus(report.id, 'investigating')}
                                disabled={updating}
                              >
                                Under Investigation
                              </Button>
                              <Button 
                                size="sm"
                                variant="outline"
                                onClick={() => updateReportStatus(report.id, 'flagged')}
                                disabled={updating}
                              >
                                <AlertCircle className="h-4 w-4 mr-2" />
                                Flag for Review
                              </Button>
                              <Button 
                                size="sm"
                                variant="outline"
                                onClick={() => updateReportStatus(report.id, 'closed')}
                                disabled={updating}
                              >
                                Close Case
                              </Button>
                            </div>
                          </div>
                        </DialogContent>
                      </Dialog>

                      {report.status === 'verified' && (
                        <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                          Forward to Authorities
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

            {/* Info Alert */}
            <Alert className="mt-8">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                This is a demo dashboard. In production, case officers would have secure authentication 
                and access controls. Reports would be processed through automated validation before human review.
              </AlertDescription>
            </Alert>
          </>
        )}
      </div>
    </div>
  );
}
