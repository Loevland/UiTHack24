> # F#ck

> > Rev - 100pts

> Prepare to embark on an adventure into the realm of functional programming. Some say that the language is so powerful that it can even be used to solve the most complex of problems. Find the flag in the following file: 

> [File](../F#ck.dll)

# Writeup

The attached file is a .NET assembly, which can be decompiled using a tool such as dnSpy. After decompiling the assembly, we end up with the following code:

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Runtime.CompilerServices;
using Microsoft.FSharp.Collections;
using Microsoft.FSharp.Core;

[CompilationMapping(/*Could not decode attribute arguments.*/)]
public static class Program
{
	[Serializable]
	internal sealed class flag_004013 : FSharpFunc<char, char>
	{
		internal static readonly flag_004013 @_instance = new flag_004013();

		[CompilerGenerated]
		[DebuggerNonUserCode]
		internal flag_004013()
		{
		}

		public override char Invoke(char c)
		{
			return (char)(c - 1);
		}
	}

	[Serializable]
	internal sealed class flag_004012_002D1 : FSharpFunc<char, char>
	{
		internal static readonly flag_004012_002D1 @_instance = new flag_004012_002D1();

		[CompilerGenerated]
		[DebuggerNonUserCode]
		internal flag_004012_002D1()
		{
		}

		public override char Invoke(char c)
		{
			return (char)(c + 1);
		}
	}

	[EntryPoint]
	public static int main(string[] args)
	{
		int num = args.Length;
		if (num < 1)
		{
			PrintfFormat<FSharpFunc<int, Unit>, TextWriter, Unit, Unit> val = (PrintfFormat<FSharpFunc<int, Unit>, TextWriter, Unit, Unit>)(object)new PrintfFormat<FSharpFunc<int, Unit>, TextWriter, Unit, Unit, int>("Expected at least one argument, got %i.");
			PrintfModule.PrintFormatLineToTextWriter<FSharpFunc<int, Unit>>(Console.Out, val).Invoke(args.Length);
		}
		else
		{
			string text = ArrayModule.Head<string>(args);
			flag_004013 @_instance;
			@_instance = flag_004013.@_instance;
			char[] array = "lano!tkc@f".ToCharArray();
			string text2 = new string(ArrayModule.Reverse<char>(ArrayModule.OfSeq<char>(SeqModule.Map<char, char>((FSharpFunc<char, char>)@_instance, SeqModule.Map<char, char>((FSharpFunc<char, char>)flag_004012_002D1.@_instance, (System.Collections.Generic.IEnumerable<char>)array)))));
			if (String.Equals(text, "D2005S"))
			{
				PrintfFormat<FSharpFunc<string, Unit>, TextWriter, Unit, Unit> val2 = (PrintfFormat<FSharpFunc<string, Unit>, TextWriter, Unit, Unit>)(object)new PrintfFormat<FSharpFunc<string, Unit>, TextWriter, Unit, Unit, string>("TD{%s}");
				PrintfModule.PrintFormatLineToTextWriter<FSharpFunc<string, Unit>>(Console.Out, val2).Invoke(text2);
			}
		}
		return 0;
	}
}
```

The code is a simple .NET assembly with a single entry point. The program takes a single argument and checks if it is equal to "D2005S". If it is, the program will print the result of a series of transformations on the string array. The transformations are as follows:

1. Reverse the array
2. Increment each character by 1
3. Decrement each character by 1

The result of these transformations is the flag: 

```
UiTHack24{f@ckt!onal}
```