use clap::Parser;
use execute;
use create_process_w;
use wintrap::{trap, Signal::CtrlC, Signal::CtrlBreak};

/// Repeat a command
#[derive(Parser)]
#[derive(Debug)]
struct Arguments {
    /// The command to run
    cmd: String,

    /// Do not print to console
    #[arg(short, long)]
    quiet: bool,

    /// Do not use shell
    #[arg(short, long)]
    direct: bool,

    ///Maximum number of times to repeat
    #[arg(short = 'n', long)]
    attempts: Option<usize>,

    /// Passthrough Ctrl+Break
    #[arg(short = 'b', long)]
    no_break: bool,

    /// Repeat the command until it succeeds
    #[arg(short = '0', long)]
    till_success: bool,

    /// Repeat the command until it fails
    #[arg(short = '1', long)]
    till_failure: bool,
}

fn run(cmd: &String, direct: &bool) -> i64 {
    if *direct {
        create_process_w::Command::new(cmd).status().expect("Failed to run").code().into()
    } else {
        match execute::shell(cmd).status().expect("Failed to run").code() {
            Some(code) => code.into(),
            None => 0xc000013a,
        }
    }
}

fn main() {
    let args = Arguments::parse();
    // println!("{:?}", &args);

    for idx in 1.. {
        match args.attempts {
            Some(n) if idx > n => {
                println!("Reached maximum number of attempts {}", n);
                break;
            },
            _ => {},
        };
        if idx > 1 && !args.quiet {
            if args.till_failure {
                println!("Repeating...");
            } else if args.till_success {
                println!("Retrying...");
            }
            println!("")
        }
        if !args.quiet {
            match args.attempts {
                Some(n) => println!("Running {}/{}: {}", &idx, &n, &args.cmd),
                _ => println!("Running: {}", &args.cmd),
            };
        }
        let return_code = trap(
            if args.no_break {&[CtrlC, CtrlBreak]} else {&[CtrlC]},
            |signal| {if signal == CtrlBreak {println!("^Break");}},
            || {run(&args.cmd, &args.direct)}
        ).unwrap();
        if !args.quiet {
            print!("Command exited with error code {}. ", &return_code);
        }
        if return_code == 0 && args.till_success ||
            return_code != 0 && args.till_failure {
                break;
        }
    }
}
