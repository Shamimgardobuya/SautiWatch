import { AlertCircle } from "lucide-react";
import { Button } from "./ui/button";

export function QuickExit() {
  const handleQuickExit = () => {
    // Redirect to a safe website (e.g., weather or news)
    window.location.href = "https://www.google.com";
  };

  return (
    <Button
      onClick={handleQuickExit}
      variant="destructive"
      className="fixed top-4 right-4 z-50 gap-2"
    >
      <AlertCircle className="h-4 w-4" />
      Quick Exit
    </Button>
  );
}
