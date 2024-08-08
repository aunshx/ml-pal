import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

interface ProjectCardProps {
    title: string;
    description: string;
}

export default function ProjectCard({ title, description }: ProjectCardProps) {
  return (
    <Card className="transform transition-transform duration-300 hover:scale-105">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-muted-foreground">
          Chat: Discuss project details and collaborate on next steps.
        </div>
      </CardContent>
      <CardFooter className="flex justify-end items-center">
        <Button
          variant="ghost"
          size="icon"
          className="text-muted-foreground hover:bg-muted"
        >
          <ArrowRight className="w-5 h-5" />
        </Button>
      </CardFooter>
    </Card>
  );
}
