import React from 'react';
import { useTodos } from './hooks/useTodos';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/card';
import './index.css';

function App() {
  const { todos, loading, error, addTodo, updateTodo, deleteTodo, toggleTodo } = useTodos();

  const completedCount = todos.filter(todo => todo.completed).length;
  const totalCount = todos.length;

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading todos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Todo App
          </h1>
          <p className="text-muted-foreground">
            Stay organized and get things done
          </p>
        </div>

        {error && (
          <Card className="mb-6 border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive">{error}</p>
            </CardContent>
          </Card>
        )}

        <TodoForm onSubmit={addTodo} />

        {totalCount > 0 && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">
                Progress: {completedCount} of {totalCount} completed
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${totalCount > 0 ? (completedCount / totalCount) * 100 : 0}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>
        )}

        <TodoList
          todos={todos}
          onUpdate={updateTodo}
          onDelete={deleteTodo}
          onToggle={toggleTodo}
        />
      </div>
    </div>
  );
}

export default App;