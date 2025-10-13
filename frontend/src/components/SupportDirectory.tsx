import { useState, useEffect } from "react";
import { Heart, Phone, MapPin, Search, AlertCircle } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Alert, AlertDescription } from "./ui/alert";
import { Skeleton } from "./ui/skeleton";
import { supportAPI, type SupportService, type ApiError } from "../services/api";

export function SupportDirectory() {
  const [searchTerm, setSearchTerm] = useState("");
  const [services, setServices] = useState<SupportService[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadServices();
  }, [searchTerm]);

  const loadServices = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await supportAPI.list();
      setServices(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || "Failed to load support services. Please try again later.");
    } finally {
      setLoading(false);
    }
  };
  
  const filteredServices = services.filter(service =>
    service.region.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 py-12 px-4">
      <div className="container mx-auto max-w-5xl">
        <div className="text-center mb-8">
          <Heart className="h-12 w-12 text-purple-600 mx-auto mb-4" />
          <h1>Support Network Directory</h1>
          <p className="text-muted-foreground mt-2">
            Connect with verified professionals who can provide immediate help and support
          </p>
        </div>

        {/* Search */}
        <div className="mb-8 max-w-md mx-auto">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by region, or service type..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Emergency Notice */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
          <h3 className="text-red-900 mb-2">In Immediate Danger?</h3>
          <p className="text-red-800 mb-3">
            If you are in immediate danger, call emergency services or use the 24/7 crisis hotline below.
          </p>
          <div className="flex gap-3">
            <Button className="bg-red-600 hover:bg-red-700">
              <Phone className="h-4 w-4 mr-2" />
              Emergency: 999
            </Button>
            <Button variant="outline" className="border-red-600 text-red-600">
              <Phone className="h-4 w-4 mr-2" />
              24/7 Crisis: +254 700 678 901
            </Button>
          </div>
        </div>

        {/* Error State */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {error}
              <Button 
                variant="outline" 
                size="sm" 
                className="ml-4"
                onClick={loadServices}
              >
                Try Again
              </Button>
            </AlertDescription>
          </Alert>
        )}

        {/* Loading State */}
        {loading && (
          <div className="grid md:grid-cols-2 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-20 w-full mb-4" />
                  <Skeleton className="h-10 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Services Grid */}
  {!loading && !error && (
  <div className="grid md:grid-cols-2 gap-6">
    {filteredServices.map((service) => (
      <Card key={service.id} className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="mb-2">{service.name}</CardTitle>
              <CardDescription className="flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                {service.region}
              </CardDescription>
            </div>
            {service.is_verified && (
              <Badge className="bg-green-600">Verified</Badge>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Service Type:</p>
              <div className="flex flex-wrap gap-2">
                {/* Here’s the fix: use category since your backend doesn’t provide services array */}
                <Badge variant="secondary">{service.category}</Badge>
              </div>
            </div>

            <div className="flex items-center gap-2 text-sm">
              <span className="text-muted-foreground">Phone:</span>
              <span>{service.phone_number}</span>
            </div>

            <div className="pt-2 border-t">
              <Button 
                className="w-full bg-purple-600 hover:bg-purple-700"
                onClick={() => window.location.href = `tel:${service.phone_number}`}
              >
                <Phone className="h-4 w-4 mr-2" />
                Call {service.phone_number}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    ))}
  </div>
)}


        {/* Additional Resources */}
        <div className="mt-12 bg-white rounded-lg p-6 shadow-sm">
          <h2 className="mb-4">Additional Resources</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <h3 className="mb-2">National Hotlines</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Gender Violence Hotline: 1195</li>
                <li>• Child Helpline: 116</li>
                <li>• National Police: 999</li>
              </ul>
            </div>
            <div>
              <h3 className="mb-2">Online Support</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Anonymous Chat Support (Coming Soon)</li>
                <li>• Support Group Forums (Coming Soon)</li>
                <li>• Resource Library (Coming Soon)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}