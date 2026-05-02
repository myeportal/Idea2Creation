# Chapter 8: Advanced OpenClaw Skills

## Mastering the Platform

You've learned the basics of OpenClaw and built your first automated business. Now it's time to dive deeper into advanced techniques that will make you a true OpenClaw power user. In this chapter, you'll learn custom skill development, complex workflow orchestration, performance optimization, and integration strategies.

## Custom Skill Development

### Understanding Skill Architecture

**Skill Structure:**
```
my-custom-skill/
├── SKILL.md              # Skill documentation
├── package.json          # Skill metadata and dependencies
├── index.js              # Main skill implementation
├── config/               # Configuration files
│   └── default.yaml
├── scripts/              # Executable scripts
│   ├── setup.sh
│   └── cleanup.sh
├── references/           # Reference materials
│   ├── api-docs.md
│   └── examples.md
└── tests/                # Test files
    └── basic.test.js
```

**SKILL.md Structure:**
```markdown
# Skill Name

## Description
Brief description of what the skill does.

## Usage
How to use the skill with examples.

## Configuration
Required configuration and environment variables.

## Dependencies
Any external dependencies or requirements.

## Examples
Practical examples of usage.

## API Reference
Detailed API documentation if applicable.
```

### Creating Your First Custom Skill

**Step 1: Initialize Skill Structure**
```bash
# Create skill directory
mkdir -p ~/.openclaw/skills/my-first-skill
cd ~/.openclaw/skills/my-first-skill

# Initialize package.json
cat > package.json << EOF
{
  "name": "my-first-skill",
  "version": "1.0.0",
  "description": "My first custom OpenClaw skill",
  "main": "index.js",
  "scripts": {
    "test": "node tests/basic.test.js"
  },
  "keywords": ["openclaw", "skill"],
  "author": "Your Name",
  "license": "MIT"
}
EOF
```

**Step 2: Create Skill Implementation**
```javascript
// index.js - Main skill implementation
const { Skill } = require('openclaw-sdk');

class MyFirstSkill extends Skill {
    constructor() {
        super({
            name: 'my-first-skill',
            version: '1.0.0',
            description: 'A custom skill example',
            commands: {
                greet: {
                    description: 'Greet someone',
                    parameters: {
                        name: {
                            type: 'string',
                            description: 'Name to greet',
                            required: true
                        }
                    }
                },
                processData: {
                    description: 'Process some data',
                    parameters: {
                        input: {
                            type: 'string',
                            description: 'Input data',
                            required: true
                        },
                        format: {
                            type: 'string',
                            description: 'Output format',
                            enum: ['json', 'csv', 'text'],
                            default: 'json'
                        }
                    }
                }
            }
        });
    }

    async greet(params) {
        const { name } = params;
        return {
            success: true,
            message: `Hello, ${name}! Welcome to OpenClaw.`,
            timestamp: new Date().toISOString()
        };
    }

    async processData(params) {
        const { input, format } = params;
        
        try {
            let result;
            
            switch (format) {
                case 'json':
                    result = JSON.parse(input);
                    break;
                case 'csv':
                    result = input.split('\n').map(line => line.split(','));
                    break;
                case 'text':
                    result = input.toUpperCase();
                    break;
                default:
                    throw new Error(`Unsupported format: ${format}`);
            }
            
            return {
                success: true,
                data: result,
                format,
                processedAt: new Date().toISOString()
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    // Lifecycle methods
    async onInstall() {
        console.log('MyFirstSkill installed successfully');
        return { success: true };
    }

    async onUninstall() {
        console.log('MyFirstSkill uninstalled');
        return { success: true };
    }

    async onConfigure(config) {
        console.log('Configuration updated:', config);
        return { success: true };
    }
}

module.exports = MyFirstSkill;
```

**Step 3: Create Documentation**
```markdown
# My First Skill

## Description
A demonstration skill for OpenClaw that shows basic skill development patterns.

## Usage
```bash
# Greet someone
openclaw skills run my-first-skill --command greet --name "John"

# Process data
openclaw skills run my-first-skill --command processData \
  --input '{"key": "value"}' \
  --format json
```

## Configuration
No configuration required for basic usage.

## Examples

### Basic Greeting
```bash
openclaw skills run my-first-skill --command greet --name "Alice"
```
Output:
```json
{
  "success": true,
  "message": "Hello, Alice! Welcome to OpenClaw.",
  "timestamp": "2026-04-21T14:30:00.000Z"
}
```

### Data Processing
```bash
openclaw skills run my-first-skill --command processData \
  --input "name,age,email\nJohn,30,john@example.com\nJane,25,jane@example.com" \
  --format csv
```

## API Reference

### Commands

#### greet
Greets a person by name.

**Parameters:**
- `name` (string, required): Name to greet

**Returns:**
```json
{
  "success": boolean,
  "message": string,
  "timestamp": string
}
```

#### processData
Processes input data in various formats.

**Parameters:**
- `input` (string, required): Input data to process
- `format` (string): Output format (json, csv, text). Default: json

**Returns:**
```json
{
  "success": boolean,
  "data": any,
  "format": string,
  "processedAt": string,
  "error": string (if success is false)
}
```
```

**Step 4: Create Tests**
```javascript
// tests/basic.test.js
const MyFirstSkill = require('../index.js');

describe('MyFirstSkill', () => {
    let skill;

    beforeEach(() => {
        skill = new MyFirstSkill();
    });

    test('greet command works correctly', async () => {
        const result = await skill.greet({ name: 'Test User' });
        
        expect(result.success).toBe(true);
        expect(result.message).toContain('Test User');
        expect(result.timestamp).toBeDefined();
    });

    test('processData command handles JSON', async () => {
        const input = '{"test": "data"}';
        const result = await skill.processData({ input, format: 'json' });
        
        expect(result.success).toBe(true);
        expect(result.data).toEqual({ test: 'data' });
        expect(result.format).toBe('json');
    });

    test('processData command handles CSV', async () => {
        const input = 'a,b,c\n1,2,3';
        const result = await skill.processData({ input, format: 'csv' });
        
        expect(result.success).toBe(true);
        expect(result.data).toEqual([['a', 'b', 'c'], ['1', '2', '3']]);
    });

    test('processData command handles invalid input', async () => {
        const result = await skill.processData({ 
            input: 'invalid json', 
            format: 'json' 
        });
        
        expect(result.success).toBe(false);
        expect(result.error).toBeDefined();
    });
});
```

**Step 5: Install and Test**
```bash
# Link the skill for development
openclaw skills link ~/.openclaw/skills/my-first-skill

# Test the skill
openclaw skills run my-first-skill --command greet --name "Developer"

# Run tests
cd ~/.openclaw/skills/my-first-skill
npm test
```

### Advanced Skill Patterns

**Pattern 1: Stateful Skills**
```javascript
class StatefulSkill extends Skill {
    constructor() {
        super({
            name: 'stateful-skill',
            commands: {
                setState: { /* ... */ },
                getState: { /* ... */ },
                increment: { /* ... */ }
            }
        });
        
        this.state = new Map();
        this.stateFile = 'state.json';
        this.loadState();
    }

    async setState(params) {
        const { key, value } = params;
        this.state.set(key, value);
        await this.saveState();
        
        return {
            success: true,
            message: `State ${key} set to ${value}`
        };
    }

    async getState(params) {
        const { key } = params;
        const value = this.state.get(key);
        
        return {
            success: true,
            key,
            value: value || null,
            exists: this.state.has(key)
        };
    }

    async increment(params) {
        const { key, amount = 1 } = params;
        const current = parseInt(this.state.get(key) || 0);
        const newValue = current + amount;
        
        this.state.set(key, newValue);
        await this.saveState();
        
        return {
            success: true,
            key,
            oldValue: current,
            newValue,
            increment: amount
        };
    }

    async loadState() {
        try {
            if (fs.existsSync(this.stateFile)) {
                const data = fs.readFileSync(this.stateFile, 'utf8');
                const state = JSON.parse(data);
                this.state = new Map(Object.entries(state));
            }
        } catch (error) {
            console.error('Failed to load state:', error);
        }
    }

    async saveState() {
        try {
            const stateObj = Object.fromEntries(this.state);
            fs.writeFileSync(this.stateFile, JSON.stringify(stateObj, null, 2));
        } catch (error) {
            console.error('Failed to save state:', error);
        }
    }
}
```

**Pattern 2: Scheduled Tasks**
```javascript
class ScheduledSkill extends Skill {
    constructor() {
        super({
            name: 'scheduled-skill',
            commands: {
                schedule: { /* ... */ },
                listSchedules: { /* ... */ },
                cancelSchedule: { /* ... */ }
            }
        });
        
        this.schedules = new Map();
        this.scheduler = null;
    }

    async schedule(params) {
        const { name, cron, command, args = {} } = params;
        
        // Validate cron expression
        if (!this.isValidCron(cron)) {
            return {
                success: false,
                error: 'Invalid cron expression'
            };
        }

        // Create schedule
        const job = schedule.scheduleJob(cron, async () => {
            try {
                await this.executeCommand(command, args);
            } catch (error) {
                console.error(`Schedule ${name} failed:`, error);
            }
        });

        this.schedules.set(name, {
            job,
            cron,
            command,
            args,
            createdAt: new Date(),
            lastRun: null,
            nextRun: job.nextInvocation()
        });

        return {
            success: true,
            name,
            cron,
            nextRun: job.nextInvocation(),
            message: `Schedule ${name} created successfully`
        };
    }

    async listSchedules() {
        const schedules = Array.from(this.schedules.entries()).map(([name, schedule]) => ({
            name,
            cron: schedule.cron,
            command: schedule.command,
            createdAt: schedule.createdAt,
            lastRun: schedule.lastRun,
            nextRun: schedule.nextRun
        }));

        return {
            success: true,
            schedules,
            count: schedules.length
        };
    }

    async cancelSchedule(params) {
        const { name } = params;
        
        if (!this.schedules.has(name)) {
            return {
                success: false,
                error: `Schedule ${name} not found`
            };
        }

        const schedule = this.schedules.get(name);
        schedule.job.cancel();
        this.schedules.delete(name);

        return {
            success: true,
            name,
            message: `Schedule ${name} cancelled`
        };
    }

    isValidCron(cron) {
        // Basic cron validation
        const parts = cron.split(' ');
        return parts.length === 5;
    }

    async executeCommand(command, args) {
        // Execute the scheduled command
        console.log(`Executing scheduled command: ${command}`, args);
        
        // Update last run time
        // ... implementation ...
    }
}
```

**Pattern 3: External API Integration**
```javascript
class APIIntegrationSkill extends Skill {
    constructor() {
        super({
            name: 'api-integration',
            commands: {
                fetchData: { /* ... */ },
                postData: { /* ... */ },
                webhook: { /* ... */ }
            }
        });
        
        this.cache = new Map();
        this.cacheTTL = 300000; // 5 minutes
    }

    async fetchData(params) {
        const { url, method = 'GET', headers = {}, cache = true } = params;
        
        // Check cache
        if (cache) {
            const cached = this.getFromCache(url);
            if (cached) {
                return {
                    success: true,
                    data: cached.data,
                    cached: true,
                    cachedAt: cached.timestamp
                };
            }
        }

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    'User-Agent': 'OpenClaw/1.0',
                    ...headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Cache the result
            if (cache) {
                this.setCache(url, data);
            }

            return {
                success: true,
                data,
                cached: false,
                status: response.status,
                headers: Object.fromEntries(response.headers.entries())
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                url,
                method
            };
        }
    }

    async postData(params) {
        const { url, data, headers = {} } = params;
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'OpenClaw/1.0',
                    ...headers
                },
                body: JSON.stringify(data)
            });

            const responseData = await response.json();

            return {
                success: response.ok,
                data: responseData,
                status: response.status,
                headers: Object.fromEntries(response.headers.entries())
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                url
            };
        }
    }

    async webhook(params) {
        const { url, event, data } = params;
        
        // This would typically be called by other parts of the system
        // when certain events occur
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'OpenClaw-Webhook/1.0'
                },
                body: JSON.stringify({
                    event,
                    data,
                    timestamp: new Date().toISOString(),
                    source: 'openclaw'
                })
            });

            return {
                success: response.ok,
                status: response.status,
                event,
                deliveredAt: new Date().toISOString()
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                event,
                attemptedAt: new Date().toISOString()
            };
        }
    }

    getFromCache(key) {
        const cached = this.cache.get(key);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTTL) {
            return cached;
        }
        
        // Remove expired cache
        if (cached) {
            this.cache.delete(key);
        }
        
        return null;
    }

    setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
        
        // Clean up old cache entries periodically
        this.cleanupCache();
    }

    cleanupCache() {
        const now = Date.now();
        for (const [key, value] of this.cache.entries()) {
            if (now - value.timestamp > this.cacheTTL) {
                this.cache.delete(key);
            }
        }
    }
}
```

## Complex Workflow Orchestration

### TaskFlow Advanced Usage

**Complex Workflow Definition:**
```javascript
// complex-workflow.js
const { TaskFlow } = require('openclaw-taskflow');

class ProductLaunchWorkflow extends TaskFlow {
    constructor() {
        super({
            name: 'product-launch-workflow',
            version: '1.0.0',
            description: 'Complete product launch workflow',
            states: {
                initialized: {
                    description: 'Workflow initialized',
                    transitions: ['research', 'planning']
                },
                research: {
                    description: 'Market research phase',
                    transitions: ['validation', 'back_to_planning']
                },
                validation: {
                    description: 'Idea validation',
                    transitions: ['creation', 'kill_idea']
                },
                creation: {
                    description: 'Product creation',
                    transitions: ['testing', 'back_to_validation']
                },
                testing: {
                    description: 'Quality testing',
                    transitions: ['launch_prep', 'back_to_creation']
                },
                launch_prep: {
                    description: 'Launch preparation',
                    transitions: ['launch', 'delay_launch']
                },
                launch: {
                    description: 'Product launch',
                    transitions: ['post_launch', 'emergency_stop']
                },
                post_launch: {
                    description: 'Post-launch activities',
                    transitions: ['complete', 'iterate']
                },
                complete: {
                    description: 'Workflow complete',
                    final: true
                },
                kill_idea: {
                    description: 'Idea killed',
                    final: true
                }
            },
            initial: '