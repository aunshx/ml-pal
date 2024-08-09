import Link from "next/link";
import { useRouter } from "next/router";
import {
  Plus,
  Search as SearchIcon,
  ArrowUpDown as ArrowUpDownIcon,
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import ProjectCard from "./ProjectCard";
import { usePipelineContext } from "@/context/PipelineContext";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card";
import { Loader } from "../ui/loader";

const projects = [
  {
    id: 1,
    title: "Project A",
    description: "A brief description of Project A and what it entails.",
  },
  {
    id: 2,
    title: "Project B",
    description: "A brief description of Project B and what it entails.",
  },
  {
    id: 3,
    title: "Project C",
    description: "A brief description of Project C and what it entails.",
  },
  {
    id: 4,
    title: "Project D",
    description: "A brief description of Project D and what it entails.",
  },
  {
    id: 5,
    title: "Project E",
    description: "A brief description of Project E and what it entails.",
  },
  {
    id: 6,
    title: "Project F",
    description: "A brief description of Project F and what it entails.",
  },
  {
    id: 7,
    title: "Project F",
    description: "A brief description of Project F and what it entails.",
  },
];

function AddProjectCard() {
  const { newPipelineLoading, createNewPipeline } = usePipelineContext();

  return (
      <button className="flex flex-col items-center justify-center p-6 border rounded-lg cursor-pointer transition-shadow hover:shadow-md bg-background h-full w-full" disabled={newPipelineLoading} onClick={createNewPipeline}>
        {newPipelineLoading ? (
          <div>
            <Loader />
          </div>
        ) : (
          <>
            <Plus className="h-12 w-12 text-muted-foreground mb-2" />
            <span className="text-lg font-medium text-muted-foreground">
              Add New Project
            </span>
          </>
        )}
      </button>
  );
}


const LoadingCard = () => {
  return (
    <Card className="transform transition-transform duration-300 hover:scale-105 w-full">
      <CardHeader className="w-full">
        <CardTitle className="h-6 bg-gray-200 rounded-full dark:bg-gray-700 w-full mb-4 animate-pulse">
        </CardTitle>
        <CardDescription className="h-4 bg-gray-200 rounded-full dark:bg-gray-700 w-full mb-4 animate-pulse mt-1" />
      </CardHeader>
      <CardContent>
        <div className="h-3 bg-gray-200 rounded-full dark:bg-gray-700 w-full mb-4 animate-pulse mt-2"></div>
      </CardContent>
      <CardFooter className="flex justify-end items-center">
        <div className="text-white">
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Exercit
        </div>
      </CardFooter>
    </Card>
  )
}


export default function HomeView() {
  const { loading, pipelines } = usePipelineContext();

  return (
    <div className="w-80per mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between mb-6 w-full">
        <div className="relative w-full max-w-md">
          <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search projects..."
            className="pl-10 w-full"
          />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-4">
              <ArrowUpDownIcon className="w-4 h-4 mr-2" />
              Sort by
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-[200px]" align="end">
            <DropdownMenuRadioGroup value="newest">
              <DropdownMenuRadioItem value="newest">
                Newest
              </DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="oldest">
                Oldest
              </DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="a-z">A-Z</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="z-a">Z-A</DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <>
            {projects.map((project, index) => (
              <LoadingCard
                key={index}
              />
            ))}
          </>
        ) : (
          <>
            <AddProjectCard />
            {pipelines.map((project) => (
              <ProjectCard
                key={project.pipeline_id}
                id={project.pipeline_id}
                title={project.pipeline_name ?? 'No Title'}
                description={project.pipeline_desc ?? 'No Description Provided'}
                createdAt={project.created_at}
                selection={project.selection}
                infra={project.infra}
                inferencing={project?.inferencing}
                training={project?.training}
              />
            ))}
          </>
        )}
      </div>
    </div>
  );
}
