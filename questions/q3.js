/*
*   Implement Command Pattern for Undo/Redo in a Text Editor
*/

// ===== ICommand Interface (Base Class) =====
class ICommand {
  execute() {
    throw new Error('execute() must be implemented');
  }

  undo() {
    throw new Error('undo() must be implemented');
  }
}

// ===== Receiver: TextEditor =====
class TextEditor {
  constructor() {
    this.content = '';
  }

  insert(text, position) {
    this.content =
      this.content.slice(0, position) + text + this.content.slice(position);
  }

  delete(start, length) {
    const deleted = this.content.slice(start, start + length);
    this.content =
      this.content.slice(0, start) + this.content.slice(start + length);
    return deleted;
  }

  getContent() {
    return this.content;
  }
}

// ===== Concrete Commands =====
class InsertTextCommand extends ICommand {
  constructor(editor, text, position) {
    super();
    this.editor = editor;
    this.text = text;
    this.position = position;
  }

  execute() {
    this.editor.insert(this.text, this.position);
  }

  undo() {
    this.editor.delete(this.position, this.text.length);
  }
}

class DeleteTextCommand extends ICommand {
  constructor(editor, start, length) {
    super();
    this.editor = editor;
    this.start = start;
    this.length = length;
    this.deletedText = '';
  }

  execute() {
    this.deletedText = this.editor.delete(this.start, this.length);
  }

  undo() {
    this.editor.insert(this.deletedText, this.start);
  }
}

// ===== Invoker: Command Manager (supports Redo) =====
class EditorInvoker {
  constructor() {
    this.undoStack = [];
    this.redoStack = [];
  }

  executeCommand(command) {
    command.execute();
    this.undoStack.push(command);
    this.redoStack = []; // clear redo stack on new action
  }

  undo() {
    if (this.undoStack.length > 0) {
      const cmd = this.undoStack.pop();
      cmd.undo();
      this.redoStack.push(cmd);
    }
  }

  redo() {
    if (this.redoStack.length > 0) {
      const cmd = this.redoStack.pop();
      cmd.execute();
      this.undoStack.push(cmd);
    }
  }
}

// ===== Client Code =====
const editor = new TextEditor();
const invoker = new EditorInvoker();

invoker.executeCommand(new InsertTextCommand(editor, 'Hello', 0));
console.log(editor.getContent()); // Hello

invoker.executeCommand(new InsertTextCommand(editor, ' World', 5));
console.log(editor.getContent()); // Hello World

invoker.undo();
console.log(editor.getContent()); // Hello

invoker.redo();
console.log(editor.getContent()); // Hello World

invoker.executeCommand(new DeleteTextCommand(editor, 5, 6));
console.log(editor.getContent()); // Hello

invoker.undo();
console.log(editor.getContent()); // Hello World
