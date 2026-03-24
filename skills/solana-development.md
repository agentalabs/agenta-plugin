---
description: Solana blockchain development best practices for Anchor, Metaplex, and DeFi. Auto-applies when working with Rust programs, TypeScript clients, or Solana configuration.
globs:
  - "**/*.rs"
  - "**/Anchor.toml"
  - "**/Cargo.toml"
  - "**/programs/**/*"
  - "**/app/**/*.ts"
  - "**/app/**/*.tsx"
  - "**/tests/**/*.ts"
---

# Solana Development Skill

## Overview

This skill provides best practices for Solana blockchain development using Anchor framework, Metaplex standards, and modern TypeScript tooling.

## When This Skill Applies

- Writing or reviewing Solana programs (Rust/Anchor)
- Building with Metaplex (NFTs, tokens, metadata)
- Integrating Jupiter, Helius, or other Solana protocols
- Writing TypeScript/JavaScript clients for Solana
- Testing Solana programs

## Available Tools

Use these MCP tools for Solana development:

- **Helius MCP**: Query blockchain data, get asset info, submit transactions
- **mcpdoc**: Access Solana/Helius/Jupiter documentation via llms.txt
- **Claude Context**: Semantic search across your codebase
- **E2B/Daytona**: Sandboxed execution for testing

## Program Development (Rust/Anchor)

### Framework Choice

Always use **Anchor framework** unless raw performance is critical:

```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramIdHere...");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        // Implementation
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 32)]
    pub my_account: Account<'info, MyAccount>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct MyAccount {
    pub authority: Pubkey,
}
```

### Account Validation

Always use proper constraints:

```rust
#[derive(Accounts)]
pub struct UpdateData<'info> {
    #[account(
        mut,
        has_one = authority,
        constraint = my_account.is_initialized @ ErrorCode::NotInitialized
    )]
    pub my_account: Account<'info, MyAccount>,
    pub authority: Signer<'info>,
}
```

### Program Derived Addresses (PDAs)

Use PDAs for program-owned accounts:

```rust
#[derive(Accounts)]
#[instruction(seed: String)]
pub struct CreatePda<'info> {
    #[account(
        init,
        seeds = [b"vault", seed.as_bytes()],
        bump,
        payer = user,
        space = 8 + 32 + 8
    )]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}
```

### Error Handling

Define custom errors:

```rust
#[error_code]
pub enum ErrorCode {
    #[msg("Account is not initialized")]
    NotInitialized,
    #[msg("Unauthorized access")]
    Unauthorized,
    #[msg("Arithmetic overflow")]
    Overflow,
    #[msg("Invalid amount")]
    InvalidAmount,
}
```

## Security Checklist

Before deployment, verify:

1. **Integer Overflow/Underflow**
   ```rust
   // ❌ BAD
   let result = a + b;

   // ✅ GOOD
   let result = a.checked_add(b).ok_or(ErrorCode::Overflow)?;
   ```

2. **Signer Validation**
   ```rust
   // Always verify authority
   require!(ctx.accounts.authority.key() == my_account.authority, ErrorCode::Unauthorized);
   ```

3. **Account Ownership**
   ```rust
   // Anchor does this automatically with Account<'info, T>
   // For raw accounts, check manually:
   require!(account.owner == &crate::ID, ErrorCode::InvalidOwner);
   ```

4. **Close Accounts Properly**
   ```rust
   #[account(
       mut,
       close = recipient,
       has_one = authority
   )]
   pub account_to_close: Account<'info, MyAccount>,
   ```

5. **PDA Bump Validation**
   ```rust
   // Store and verify bumps
   #[account]
   pub struct Vault {
       pub bump: u8,
   }
   ```

## TypeScript Clients

### SDK Choice

Use `@solana/web3.js` v2 for new projects:

```typescript
import { createSolanaRpc, address, lamports } from '@solana/web3.js';

const rpc = createSolanaRpc('https://mainnet.helius-rpc.com/?api-key=YOUR_KEY');
const balance = await rpc.getBalance(address('...')).send();
```

### Helius Integration

Use Helius RPC for production:

```typescript
import { Helius } from 'helius-sdk';

const helius = new Helius('YOUR_API_KEY');

// Get asset info
const asset = await helius.rpc.getAsset({ id: 'NFT_MINT_ADDRESS' });

// Get transaction history
const history = await helius.getTransactionHistory({ address: 'WALLET' });
```

### Transaction Best Practices

```typescript
// Always use priority fees during congestion
const priorityFee = await helius.rpc.getPriorityFeeEstimate({
  accountKeys: ['PROGRAM_ID'],
  options: { priorityLevel: 'High' }
});

// Implement retry logic
const MAX_RETRIES = 3;
for (let i = 0; i < MAX_RETRIES; i++) {
  try {
    const sig = await sendAndConfirmTransaction(connection, tx, [payer]);
    break;
  } catch (e) {
    if (i === MAX_RETRIES - 1) throw e;
    await sleep(1000 * (i + 1)); // Exponential backoff
  }
}
```

## Testing

### Anchor Tests

```typescript
import * as anchor from '@coral-xyz/anchor';
import { Program } from '@coral-xyz/anchor';
import { MyProgram } from '../target/types/my_program';

describe('my-program', () => {
  anchor.setProvider(anchor.AnchorProvider.env());
  const program = anchor.workspace.MyProgram as Program<MyProgram>;

  it('Initializes account', async () => {
    const myAccount = anchor.web3.Keypair.generate();

    await program.methods
      .initialize()
      .accounts({
        myAccount: myAccount.publicKey,
        user: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([myAccount])
      .rpc();

    const account = await program.account.myAccount.fetch(myAccount.publicKey);
    expect(account.authority.toString()).to.equal(provider.wallet.publicKey.toString());
  });
});
```

## Development Workflow

1. **Check documentation first**
   ```
   > What's the latest Anchor syntax for PDAs?
   ```
   Claude will use mcpdoc to fetch from solana.com/llms.txt

2. **Write code with proper validations**

3. **Run security audit**
   ```
   > /agenta:audit
   ```
   Uses Trail of Bits Solana scanner

4. **Test on devnet**
   ```bash
   anchor test --provider.cluster devnet
   ```

5. **Deploy with priority fees**
   ```bash
   anchor deploy --provider.cluster mainnet --priority-fee 10000
   ```

## Common Patterns

### Token Transfers (SPL)

```rust
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    let cpi_accounts = Transfer {
        from: ctx.accounts.from.to_account_info(),
        to: ctx.accounts.to.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };
    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_ctx = CpiContext::new(cpi_program, cpi_accounts);
    token::transfer(cpi_ctx, amount)?;
    Ok(())
}
```

### Cross-Program Invocation (CPI)

```rust
use anchor_lang::solana_program::program::invoke_signed;

pub fn cpi_example(ctx: Context<CpiExample>, bump: u8) -> Result<()> {
    let seeds = &[b"authority".as_ref(), &[bump]];
    let signer_seeds = &[&seeds[..]];

    invoke_signed(
        &instruction,
        &[ctx.accounts.target_program.to_account_info()],
        signer_seeds,
    )?;
    Ok(())
}
```

## Resources

- **Solana Docs**: Use `mcpdoc` → Solana
- **Helius Docs**: Use `mcpdoc` → Helius
- **Jupiter Docs**: Use `mcpdoc` → Jupiter
- **Anchor Book**: https://book.anchor-lang.com
- **Metaplex Docs**: Use Context7 plugin
