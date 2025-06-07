import React from 'react';
import TodoItem from './TodoItem';

const TodoList = ({ todos, onUpdate, onDelete, onToggle }) => {
  if (todos.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground text-lg">No todos yet!</p>
        <p className="text-muted-foreground">Add one above to get started.</p>
      </div>
    );
  }

  // Sort todos: incomplete first, then by priority, then by creation date
  const sortedTodos = [...todos].sort((a, b) => {
    if (a.completed !== b.completed) {
      return a.completed - b.completed;
    }
    
    const priorityOrder = { high: 3, medium: 2, low: 1 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    }
    
    return new Date(b.created_at) - new Date(a.created_at);
  });

  return (
    <div className="space-y-3">
      {sortedTodos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onUpdate={onUpdate}
          onDelete={onDelete}
          onToggle={onToggle}
        />
      ))}
    </div>
  );
};

export default TodoList;