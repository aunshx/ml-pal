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
import moment from 'moment'
interface ProjectCardProps {
    id: number;
    createdAt: Date;
    title?: string;
    description?: string;
    selection: boolean;
    infra: boolean;
    inferencing?: boolean | null;
    training?: boolean | null;
}

export default function ProjectCard(props: ProjectCardProps) {
  const { id, title, description, createdAt, selection, infra, inferencing, training } = props;

  const dateString = createdAt.toLocaleString();

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
      <CardFooter className="flex justify-between items-center">
        <div className="text-xs text-gray-400">
          {dateString}
        </div>
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
