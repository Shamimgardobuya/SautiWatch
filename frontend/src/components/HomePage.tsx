import { Link } from "react-router-dom";
import { Shield, Users, Heart, FileText } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";

export function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Shield className="h-12 w-12 text-blue-600" />
            <h1 className="text-4xl">SautiWatch</h1>
          </div>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Your voice matters. Report safely, get help, and drive accountability in your community.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link to="/report">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Report Anonymously
              </Button>
            </Link>
            <Link to="/support">
              <Button size="lg" variant="outline">
                Find Support
              </Button>
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <Card>
            <CardHeader>
              <Shield className="h-10 w-10 text-blue-600 mb-2" />
              <CardTitle>Safe Reporting</CardTitle>
              <CardDescription>
                Share your experience anonymously with complete confidentiality. Your identity is protected.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Heart className="h-10 w-10 text-purple-600 mb-2" />
              <CardTitle>Immediate Support</CardTitle>
              <CardDescription>
                Connect with verified counsellors, therapists, and healthcare professionals who can help.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Users className="h-10 w-10 text-green-600 mb-2" />
              <CardTitle>Community Accountability</CardTitle>
              <CardDescription>
                Help identify patterns and alert authorities when action is needed in your area.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* How It Works */}
        <div className="bg-white rounded-lg p-8 shadow-sm mb-12">
          <h2 className="text-center mb-8">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 text-blue-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                1
              </div>
              <h3 className="mb-2">Report Safely</h3>
              <p className="text-muted-foreground">
                Fill out a simple form with details about the incident. All information is encrypted and anonymous.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 text-purple-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                2
              </div>
              <h3 className="mb-2">Get Support</h3>
              <p className="text-muted-foreground">
                Access verified support networks including counsellors, therapists, and healthcare professionals.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 text-green-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                3
              </div>
              <h3 className="mb-2">Drive Action</h3>
              <p className="text-muted-foreground">
                Your report helps authorities identify patterns and take coordinated action in affected areas.
              </p>
            </div>
          </div>
        </div>

        {/* Additional Links */}
        <div className="grid md:grid-cols-2 gap-6">
          <Link to="/testimonials">
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Success Stories
                </CardTitle>
                <CardDescription>
                  Read anonymous testimonials from survivors who found help through SautiWatch.
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>

          <Link to="/admin">
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Authority Portal
                </CardTitle>
                <CardDescription>
                  For case officers and authorities to review and respond to reports.
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>
        </div>

        {/* Safety Notice */}
        <div className="mt-12 bg-amber-50 border border-amber-200 rounded-lg p-6">
          <h3 className="text-amber-900 mb-2">Your Safety First</h3>
          <p className="text-amber-800">
            If you're in immediate danger, please call emergency services. Use the "Quick Exit" button 
            at the top right to quickly leave this site if needed. The button will take you to a safe website.
          </p>
        </div>
      </div>
    </div>
  );
}
