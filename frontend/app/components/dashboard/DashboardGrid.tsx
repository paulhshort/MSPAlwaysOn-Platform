'use client';

import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';

interface DashboardGridProps {
  children: React.ReactNode[];
  onReorder?: (newOrder: number[]) => void;
}

const DashboardGrid: React.FC<DashboardGridProps> = ({ children, onReorder }) => {
  const [widgets, setWidgets] = useState(
    React.Children.map(children, (child, index) => ({
      id: `widget-${index}`,
      content: child,
    }))
  );

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const items = Array.from(widgets);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setWidgets(items);

    if (onReorder) {
      const newOrder = items.map((item, index) => {
        const originalIndex = parseInt(item.id.split('-')[1]);
        return originalIndex;
      });
      onReorder(newOrder);
    }
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="dashboard-grid" direction="horizontal">
        {(provided) => (
          <div
            {...provided.droppableProps}
            ref={provided.innerRef}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {widgets.map((widget, index) => (
              <Draggable key={widget.id} draggableId={widget.id} index={index}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    className={`${
                      snapshot.isDragging ? 'opacity-70 shadow-xl' : ''
                    } transition-all duration-200`}
                  >
                    <div
                      {...provided.dragHandleProps}
                      className="cursor-move bg-slate-800 rounded-t-lg px-3 py-1.5 text-xs text-slate-400 border-b border-slate-700 flex items-center justify-between"
                    >
                      <span>Drag to reorder</span>
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                    </div>
                    {widget.content}
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
};

export default DashboardGrid;
