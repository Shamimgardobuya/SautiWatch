import { useState, useEffect } from "react";
import { Heart, Quote, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Alert, AlertDescription } from "./ui/alert";
import { Skeleton } from "./ui/skeleton";
import { testimonialsAPI, type Testimonial, type ApiError } from "../services/api";

export function Testimonials() {
  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTestimonials();
  }, []);

  const loadTestimonials = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await testimonialsAPI.list();
      setTestimonials(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || "Failed to load testimonials. Please try again later.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <Heart className="h-12 w-12 text-purple-600 mx-auto mb-4" />
          <h1>Stories of Hope & Healing</h1>
          <p className="text-muted-foreground mt-2 max-w-2xl mx-auto">
            Anonymous testimonials from survivors who found help through SautiWatch. 
            Their courage inspires us to continue this important work.
          </p>
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
                onClick={loadTestimonials}
              >
                Try Again
              </Button>
            </AlertDescription>
          </Alert>
        )}

        {/* Loading State */}
        {loading && (
          <div className="grid md:grid-cols-2 gap-6 mb-12">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Card key={i}>
                <CardContent className="pt-6">
                  <Skeleton className="h-8 w-8 mb-4" />
                  <Skeleton className="h-20 w-full mb-6" />
                  <Skeleton className="h-6 w-3/4" />
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Testimonials Grid */}
        {!loading && !error && (
          <div className="grid md:grid-cols-2 gap-6 mb-12">
            {testimonials.map((testimonial) => (
              <Card key={testimonial.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="pt-6">
                  <Quote className="h-8 w-8 text-purple-300 mb-4" />
                  <p className="text-muted-foreground italic mb-6">
                    "{testimonial.quote}"
                  </p>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge variant="secondary">{testimonial.type}</Badge>
                    <span className="text-sm text-muted-foreground">•</span>
                    <span className="text-sm text-muted-foreground">{testimonial.location}</span>
                    <span className="text-sm text-muted-foreground">•</span>
                    <span className="text-sm text-muted-foreground">{testimonial.year}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Call to Action */}
        <div className="bg-white rounded-lg p-8 shadow-sm text-center">
          <h2 className="mb-4">You Are Not Alone</h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            Every survivor's journey is unique, but you don't have to face it alone. 
            SautiWatch is here to connect you with the support and resources you need to heal and rebuild.
          </p>
          <div className="flex gap-4 justify-center">
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

        {/* Share Your Story */}
        <div className="mt-8 bg-purple-50 border border-purple-200 rounded-lg p-6">
          <h3 className="text-purple-900 mb-2">Share Your Story</h3>
          <p className="text-purple-800">
            If you've found healing through SautiWatch and would like to share your anonymous story 
            to inspire others, please contact our support team. Your courage can give hope to someone 
            who's still struggling.
          </p>
        </div>
      </div>
    </div>
  );
}
