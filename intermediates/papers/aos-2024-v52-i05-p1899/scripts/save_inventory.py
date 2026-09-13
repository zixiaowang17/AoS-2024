# -*- coding: utf-8 -*-
"""Restore twenty complete original Theorem statements from registered arXiv v1.

Running this script reproduces a transcription; source review is a separate gate.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p1899'
SHA='93b9db86f7125d5eb9a7d7aba007cdd9eb2802c5fcd490081016308a2cd03fe1'
URL='https://arxiv.org/pdf/2207.00120v1'
NUMBERS=['3.1','3.2','4.1','4.2','4.3','4.4','4.5','4.6','5.1','5.2','5.3','5.4','5.5','5.6','6.1','6.2','6.3','6.4','6.5','6.6']
PAGES=[[8],[9],[11],[11],[12],[12],[13],[14],[15],[15,16],[16],[17],[18],[18],[20],[20,21],[21],[21],[22],[22]]
STATEMENTS=[r'''Suppose that $\emptyset\notin\Psi$ and let $\gamma,\delta\in(0,1)$.

(i) $\chi^*\in\mathcal C_\Psi(\gamma,\delta)$ when
\[
A_e\geq a_e|\mathcal K|/\delta\quad\text{and}\quad B_e\geq b_e|\mathcal K|/\gamma\qquad\forall e\in\mathcal K.
\]
(ii) If, also, $\Psi=\Psi_{m,m}$ for some $m\in(0,|\mathcal K|)$, then $\chi^*\in\mathcal C_\Psi(\gamma,\delta)$ when
\[
A_e\geq a_e|\mathcal K|/(\gamma\wedge\delta)\quad\text{and}\quad B_e\geq b_e|\mathcal K|/(\gamma\wedge\delta)\qquad\forall e\in\mathcal K.
\]''',r'''Suppose that $\emptyset\in\Psi$ and let $\alpha,\beta,\gamma,\delta\in(0,1)$.

(i) $\chi^*_{\mathrm{det}}\in\mathcal D_\Psi(\alpha,\beta)$ when
\[
C_e\geq c_e/\beta\quad\text{and}\quad D_e\geq d_e|\mathcal K|/\alpha\qquad\forall e\in\mathcal K.
\]
(ii) $\chi^*_{\mathrm{fwer}}\in\mathcal E_\Psi(\gamma,\delta)$ when
\[
A_e\geq(a_e\vee c_e)(|\mathcal K|+1)/\delta\quad\text{and}\quad B_e\geq(b_e\vee d_e)|\mathcal K|/\gamma\qquad\forall e\in\mathcal K.
\]
If, also, $s_e=s'_e=e$ for every $e\in\mathcal K$, then $\chi^*_{\mathrm{fwer}}\in\mathcal E_\Psi(\gamma,\delta)$ when
\[
A_e\geq a_e|\mathcal K|/\delta\quad\text{and}\quad B_e\geq b_e|\mathcal K|/\gamma\qquad\forall e\in\mathcal K.
\]
(iii) $\chi^*\in\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)$ when $\{C_e,D_e\}_{e\in\mathcal K}$ are as in (i) and $\{A_e,B_e\}_{e\in\mathcal K}$ as in Theorem 3.1.''',r'''Suppose that (12) holds, $\emptyset\notin\Psi$, and let $P\in\mathcal P_\Psi$. Then, as $\gamma,\delta\to0$,
\[
\mathbb E_P[T^*]\lesssim\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_{\Psi,e};s'_e)}\right\}\bigvee\max_{e\notin\mathcal A(P)}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e};s'_e)}\right\}.
\]''',r'''Suppose that (12) holds, $\emptyset\in\Psi$, and let $P\in\mathcal P_\Psi$.

(i) If $P\in\mathcal H_0$, then
\[
\mathbb E_P[T^*_{\mathrm{det}}],\mathbb E_P[T^*]\lesssim\max_{e\in\mathcal K}\left\{\frac{|\log\beta|}{\mathcal I(P,\mathcal G_{\Psi,e};s_e)}\right\}\quad\text{as }\beta\to0,
\]
\[
\mathbb E_P[T^*_{\mathrm{fwer}}]\lesssim\max_{e\in\mathcal K}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e};s_e)}\right\}\quad\text{as }\delta\to0.
\]
(ii) If $P\notin\mathcal H_0$, then
\[
\mathbb E_P[T^*_{\mathrm{det}}]\lesssim\min_{e\in\mathcal A(P)}\left\{\frac{|\log\alpha|}{\mathcal I(P,\mathcal H_0;s_e)}\right\}\quad\text{as }\alpha\to0,
\]
\[
\mathbb E_P[T^*_{\mathrm{fwer}}]\lesssim\min_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_0;s_e)}\right\}\bigvee\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_{\Psi,e};s'_e)}\right\}\bigvee\max_{e\notin\mathcal A(P)}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e};s'_e)}\right\}\quad\text{as }\gamma,\delta\to0,
\]
\[
\mathbb E_P[T^*]\lesssim\min_{e\in\mathcal A(P)}\left\{\frac{|\log\alpha|}{\mathcal I(P,\mathcal H_0;s_e)}\right\}\bigvee\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_{\Psi,e};s'_e)}\right\}\bigvee\max_{e\notin\mathcal A(P)}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e};s'_e)}\right\}\quad\text{as }\alpha,\gamma,\delta\to0.
\]''',r'''Suppose that $\emptyset\notin\Psi$, $P\in\mathcal P_\Psi$, and let the isolation subsystems be selected such that
\[
\min_{e\in\mathcal A(P)}\mathcal I(P,\mathcal H_{\Psi,e};s'_e)=\min_{e\in\mathcal A(P)}\mathcal I(P,\mathcal H_{\Psi,e}),
\]
(15)
\[
\min_{e\notin\mathcal A(P)}\mathcal I(P,\mathcal G_{\Psi,e};s'_e)=\min_{e\notin\mathcal A(P)}\mathcal I(P,\mathcal G_{\Psi,e}),
\]
(16)
which is trivially the case when $s'_e=[K]$ for every $e\in\mathcal K$. Then, as $\gamma,\delta\to0$,
\[
\mathbb E_P[T^*]\sim\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_{\Psi,e})}\right\}\bigvee\max_{e\notin\mathcal A(P)}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal C_\Psi(\gamma,\delta)\}.
\]
When, in particular, $\Psi=\Psi_{m,m}$ for some $m\in(0,|\mathcal K|)$, then, as $\gamma,\delta\to0$,
\[
\mathbb E_P[T^*]\sim\frac{|\log(\gamma\wedge\delta)|}{\mathcal I(P,\mathcal P_\Psi\setminus\{P\})}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal C_\Psi(\gamma,\delta)\}.
\]''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal H_0$, and let the detection subsystems be selected such that
\[
\min_{e\in\mathcal K}\mathcal I(P,\mathcal G_{\Psi,e};s_e)=\min_{e\in\mathcal K}\mathcal I(P,\mathcal G_{\Psi,e}),
\]
(17)
which is trivially the case when $s_e=[K]$ for every $e\in\mathcal K$. Then, as $\alpha,\beta\to0$,
\[
\mathbb E_P[T^*_{\mathrm{det}}]\sim\max_{e\in\mathcal K}\left\{\frac{|\log\beta|}{\mathcal I(P,\mathcal G_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal D_\Psi(\alpha,\beta)\},
\]
as $\alpha,\beta\to0$, while $\gamma$ and $\delta$ are either fixed or go to $0$,
\[
\mathbb E_P[T^*]\sim\max_{e\in\mathcal K}\left\{\frac{|\log\beta|}{\mathcal I(P,\mathcal G_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)\},
\]
and as $\gamma,\delta\to0$,
\[
\mathbb E_P[T^*_{\mathrm{fwer}}]\sim\max_{e\in\mathcal K}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal E_\Psi(\gamma,\delta)\}.
\]''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal P_\Psi\setminus\mathcal H_0$, and let the detection subsystems be selected so that
\[
\max_{e\in\mathcal A(P)}\mathcal I(P,\mathcal H_0;s_e)=\mathcal I(P,\mathcal H_0),
\]
(18)
which is trivially the case when $s_e=[K]$ for some $e\in\mathcal A(P)$. Then, as $\alpha,\beta\to0$,
\[
\mathbb E_P[T^*_{\mathrm{det}}]\sim\frac{|\log\alpha|}{\mathcal I(P,\mathcal H_0)}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal D_\Psi(\alpha,\beta)\},
\]
and, as $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\alpha|\gg|\log\gamma|\vee|\log\delta|$,
\[
\mathbb E_P[T^*]\sim\frac{|\log\alpha|}{\mathcal I(P,\mathcal H_0)}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)\}.
\]
If, also, the isolation subsystems are selected so that (15) holds, then, as $\gamma,\delta\to0$ such that $|\log\gamma|\gg|\log\delta|$,
\[
\mathbb E_P[T^*_{\mathrm{fwer}}]\sim\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_0)\wedge\mathcal I(P,\mathcal H_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal E_\Psi(\gamma,\delta)\}.
\]''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal P_\Psi\setminus\mathcal H_0$, and let the detection subsystems be selected so that (18) holds, and let the isolation subsystems be selected so that (15) - (16) hold. Then, as $\gamma,\delta\to0$,
\[
\mathbb E_P[T^*_{\mathrm{fwer}}]\sim\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_0)\wedge\mathcal I(P,\mathcal H_{\Psi,e})}\right\}\bigvee\max_{e\notin\mathcal A(P)}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal E_\Psi(\gamma,\delta)\},
\]
and, as $\alpha,\beta,\gamma,\delta\to0$,
\[
\mathbb E_P[T^*]\sim\frac{|\log\alpha|}{\mathcal I(P,\mathcal H_0)}\bigvee\max_{e\in\mathcal A(P)}\left\{\frac{|\log\gamma|}{\mathcal I(P,\mathcal H_{\Psi,e})}\right\}\bigvee\max_{e\notin\mathcal A(P)}\left\{\frac{|\log\delta|}{\mathcal I(P,\mathcal G_{\Psi,e})}\right\}\sim\inf\{\mathbb E_P[T]:(T,D)\in\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)\}.
\]''',r'''Suppose that either $s'_k=\{k\}$ $\forall k\in[K]$, or $s'_k=[K]$ $\forall k\in[K]$. When $l=0$, suppose also that either $s_k=\{k\}$ $\forall k\in[K]$, or $s_k=[K]$ $\forall k\in[K]$. Then:
\[
D_{\mathrm{iso}}(T)=\{i_1(T),\ldots,i_{l\vee p(T)\wedge u}(T)\}\quad\text{for }T\in\{T^*,T^*_{\mathrm{fwer}}\},
\]
with the understanding that if $l=p(T)=0$, then $D_{\mathrm{iso}}(T)=\emptyset$.''',r'''Suppose that $l\geq1$ and let $s'_k=[K]$ for every $k\in[K]$.

(i) If $\ell=u<K$, then
\[
T^*=\inf\{n\in\mathbb N:\Lambda_{(u)}(n)\geq\Lambda_{(u+1)}(n)\max\{A,B\}\}.
\]
(ii) If $l<u\leq K$, then
\[
T^*=\begin{cases}T_1\wedge T_2\wedge T_4\wedge T_5\wedge T_6&\text{if }u<K\\T_1\wedge T_2\wedge T_3&\text{if }u=K,\end{cases}
\]
where
\[
\begin{aligned}
T_1&:=\inf\{n\in\mathbb N:p(n)<l\quad\text{and}\quad\Lambda_{(l)}(n)\geq\Lambda_{(l+1)}(n)\max\{A,B\}\},\\
T_2&:=\inf\{n\in\mathbb N:p(n)=l\quad\text{and}\quad\Lambda_{(l+1)}(n)\leq\min\{1/A,\Lambda_{(l)}(n)/B\}\},\\
T_3&:=\inf\{n\in\mathbb N:p(n)>l\quad\text{and}\quad\Lambda_k(n)\notin(1/A,B)\quad\forall k\in[K]\},\\
T_4&:=\inf\{n\in\mathbb N:p(n)\in(l,u)\quad\text{and}\quad\Lambda_k(n)\notin(1/A,B)\quad\forall k\in[K]\},\\
T_5&:=\inf\{n\in\mathbb N:p(n)=u\quad\text{and}\quad\Lambda_{(u)}(n)\geq\max\{B,A\Lambda_{(u+1)}(n)\}\},\\
T_6&:=\inf\{n\in\mathbb N:p(n)>u\quad\text{and}\quad\Lambda_{(u)}(n)\geq\Lambda_{(u+1)}(n)\max\{A,B\}\}.
\end{aligned}
\]''',r'''Suppose that $l=0$ and $s_k=[K]$ for every $k\in[K]$. Then, the stopping times, $T_0$ and $T_{\mathrm{det}}$, defined as in Subsection 3.2.2, take the following form:
\[
T_0=\inf\{n\in\mathbb N:\Lambda_{(1)}(n)\leq1/C\},\qquad T_{\mathrm{det}}=\inf\{n\in\mathbb N:\prod_{i=1}^{p(n)\wedge u}\Lambda_{(i)}(n)\geq D\}.
\]
If, also, $s'_k=[K]$ for every $k\in[K]$, then
\[
T_{\mathrm{joint}}=\begin{cases}T_1\wedge T_3\wedge T_4\wedge T_5&\text{if }u<K\\T_1\wedge T_2&\text{if }u=K,\end{cases}
\]
where
\[
\begin{aligned}
T_1&=\inf\{n\in\mathbb N:\Lambda_{(1)}(n)\geq D,\quad\Lambda_{(2)}(n)\leq\min\{1/A,\Lambda_{(1)}(n)/B\}\},\\
T_2&=\inf\{n\in\mathbb N:p(n)>1,\quad\prod_{i=1}^{p(n)}\Lambda_{(i)}(n)\geq D,\quad\Lambda_k(n)\notin(1/A,B)\quad\forall k\in[K]\},\\
T_3&=\inf\{n\in\mathbb N:p(n)\in(1,u),\quad\prod_{i=1}^{p(n)}\Lambda_{(i)}(n)\geq D,\quad\Lambda_k(n)\notin(1/A,B)\quad\forall k\in[K]\},\\
T_4&=\inf\{n\in\mathbb N:p(n)=u,\quad\prod_{i=1}^u\Lambda_{(i)}(n)\geq D,\quad\Lambda_{(u)}(n)\geq\max\{B,A\Lambda_{(u+1)}(n)\}\},\\
T_5&=\inf\{n\in\mathbb N:p(n)>u,\quad\prod_{i=1}^u\Lambda_{(i)}(n)\geq D,\quad\Lambda_{(u)}(n)\geq\Lambda_{(u+1)}(n)\max\{A,B\}\}.
\end{aligned}
\]''',r'''Suppose that $l=0$ and $s_k=\{k\}$ for every $k\in[K]$. Then $\chi^*_{\mathrm{fwer}}$ is asymptotically optimal, as $\gamma,\delta\to0$, under every $P\in\mathcal P_\Psi$

(i) when $u=K$ and $s'_k=\{k\}$ for every $k\in[K]$, in which case
\[
T^*_{\mathrm{fwer}}=\inf\{n\in\mathbb N:\Lambda_k(n)\notin(1/A,B)\quad\forall k\in[K]\},
\]
(ii) when $u<K$ and $s'_k=[K]$ for every $k\in[K]$, in which case
\[
T^*_{\mathrm{fwer}}=T_0\wedge T_1\wedge T_2\wedge T_3\wedge T_4,
\]
where
\[
\begin{aligned}
T_0&=\inf\{n\in\mathbb N:\Lambda_{(1)}(n)\leq1/A\},\\
T_1&=\inf\{n\in\mathbb N:\Lambda_{(1)}(n)\geq B,\quad\Lambda_{(2)}(n)\leq\min\{1/A,\Lambda_{(1)}(n)/B\}\},\\
T_2&=\inf\{n\in\mathbb N:p(n)\in(1,u),\quad\Lambda_{(1)}(n)\geq B,\quad\Lambda_k(n)\notin(1/A,B)\quad\forall k\in[K]\},\\
T_3&=\inf\{n\in\mathbb N:p(n)=u,\quad\Lambda_{(u)}(n)\geq\max\{B,A\Lambda_{(u+1)}(n)\}\},\\
T_4&=\inf\{n\in\mathbb N:p(n)>u,\quad\Lambda_{(1)}(n)\geq B,\quad\Lambda_{(u)}(n)\geq\Lambda_{(u+1)}(n)\max\{A,B\}\}.
\end{aligned}
\]''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal P_\Psi\setminus\mathcal H_0$ and $s'_k=\{k\}$ for every $k\in[K]$.

(i) If $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\gamma|\gg|\log\alpha|\vee|\log\delta|$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\frac{\min_{\{k\}\in\mathcal A(P)}\mathcal I(P,\mathcal H_{\Psi,k})}{\min_{\{k\}\in\mathcal A(P)}\mathcal I(P^k,\mathcal H^k)}.
\]
If, also, $\Psi=\Psi_{0,u}$, $|\mathcal A(P)|>1$, and there is a source that is independent of the other ones under $P$ and achieves $\min_{\{k\}\in\mathcal A(P)}\mathcal I(P^k,\mathcal H^k)$, then
\[
\operatorname{ARE}_P[\chi^*]=1.
\]
(ii) If $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\delta|\gg|\log\alpha|\vee|\log\gamma|$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\frac{\min_{\{k\}\notin\mathcal A(P)}\mathcal I(P,\mathcal G_{\Psi,k})}{\min_{\{k\}\notin\mathcal A(P)}\mathcal I(P^k,\mathcal G^k)}.
\]
If also $\Psi=\Psi_{0,u}$, $|\mathcal A(P)|<u$, and there is a source that is independent of the other ones under $P$ and achieves $\min_{\{k\}\notin\mathcal A(P)}\mathcal I(P^k,\mathcal G^k)$, then
\[
\operatorname{ARE}_P[\chi^*]=1.
\]''',r'''Suppose that $\emptyset\in\Psi$ and $s_k=\{k\}$ for every $k\in[K]$.

(i) If $P\in\mathcal P_\Psi\setminus\mathcal H_0$ and $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\alpha|\gg|\log\gamma|\vee|\log\delta|$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\min_{\{k\}\in\mathcal A(P)}\left\{\frac{\mathcal I(P,\mathcal H_0)}{\mathcal I(P^k,\mathcal H^k)}\right\}.
\]
If, also, there is exactly one signal that is independent of the other sources under $P$, then
\[
\operatorname{ARE}_P[\chi^*]=1.
\]
(ii) If $P\in\mathcal H_0$ and $\alpha,\beta\to0$, while $\gamma$ and $\delta$ are either fixed or go to $0$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\frac{\min_{k\in[K]}\mathcal I(P,\mathcal G_{\Psi,k})}{\min_{k\in[K]}\mathcal I(P^k,\mathcal G^k)}.
\]
If, also, $\Psi_{1,1}\subseteq\Psi$, and there is a source that is independent of the other ones under $P$ and achieves $\min_{k\in[K]}\mathcal I(P^k,\mathcal G^k)$, then
\[
\operatorname{ARE}_P[\chi^*]=1.
\]''',r'''Suppose that (23) holds and $\Psi=\Psi_{\mathrm{dis}}$. If $s_e=[K]$ for every $e\in\mathcal K$, then
\[
T_0=\inf\{n\in\mathbb N:\Lambda_{(1)}(n)\leq1/C\},
\]
\[
T_{\mathrm{det}}=\inf\left\{n\in\mathbb N:\max_{\substack{B\subseteq\{i_1(n),\ldots,i_{p(n)}(n)\},\ B\in\Psi}}\prod_{e\in B}\Lambda_e(n)\geq D\right\},
\]
where $T_0$ and $T_{\mathrm{det}}$ are defined as in Subsection 3.2.2.''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal P_\Psi\setminus\mathcal H_0$, and $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\gamma|\gg|\log\alpha|\vee|\log\delta|$.

(i) If, for every $e\in\mathcal A(P)$, there is an $l\in[L(P)]$ so that $s'_e\supseteq v_l\supseteq e$, then $\operatorname{ARE}_P[\chi^*]=1$.

(ii) If $s'_e=e$ for every $e\in\mathcal K$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\frac{\min_{e\in\mathcal A(P)}\mathcal I(P,\mathcal H_{\Psi,e})}{\min_{e\in\mathcal A(P)}\mathcal I(P^e,\mathcal H^e)}.
\]
Moreover, $\operatorname{ARE}_P[\chi^*]=1$ when one of the following set of conditions is satisfied:

• (23) holds, $\Psi=\Psi_{\mathrm{dis}}$, $|\mathcal A(P)|>1$,

• $\Psi$ is either $\Psi_{\mathrm{dis}}$, or $\Psi_{\mathrm{clus}}$, or the powerset of $\mathcal K$, $L(P)>1$, and there is a pair of data sources that is independent of all other data sources under $P$ and achieves
\[
\min_{e\in\mathcal A(P)}\mathcal I(P^e,\mathcal H^e).
\]''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal P_\Psi\setminus\mathcal H_0$, and $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\delta|\gg|\log\alpha|\vee|\log\gamma|$.

(i) $\operatorname{ARE}_P[\chi^*]=1$ when, for every $e=\{i,j\}\notin\mathcal A(P)$,
\[
s'_e\supseteq\begin{cases}
v_l&\text{if }v_l\supseteq e\quad\text{for some }l\in[L(P)],\\
v_l\cup v_{l'}&\text{if }i\in v_l\quad\text{and }j\in v_{l'}\quad\text{for some }l\ne l',\quad l,l'\in[L(P)],\\
e\cup v_l&\text{if }i\text{ or }j\in v_0\quad\text{and }e\setminus v_0\in v_l\quad\text{for some }l\in[L(P)],\\
e&\text{if }v_0\supseteq e.
\end{cases}
\]
(ii) If $s'_e=e$ for every $e\in\mathcal K$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\frac{\min_{e\notin\mathcal A(P)}\mathcal I(P,\mathcal G_{\Psi,e})}{\min_{e\notin\mathcal A(P)}\mathcal I(P^e,\mathcal G^e)}.
\]
Moreover, $\operatorname{ARE}_P[\chi^*]=1$ when $\Psi$ is either $\Psi_{\mathrm{dis}}$, or $\Psi_{\mathrm{clus}}$, or the powerset of $\mathcal K$, and there is a pair of data sources that is independent of all other data sources under $P$ and achieves
\[
\min_{e\notin\mathcal A(P)}\mathcal I(P^e,\mathcal G^e).
\]''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal P_\Psi\setminus\mathcal H_0$, and $\alpha,\beta,\gamma,\delta\to0$ such that $|\log\alpha|\gg|\log\gamma|\vee|\log\delta|$.

(i) If there is an $e\in\mathcal A(P)$ such that $s_e\supseteq v_1\cup\ldots\cup v_{L(P)}$, then $\operatorname{ARE}_P[\chi^*]=1$.

(ii) If $s_e=e$ for every $e\in\mathcal K$, then
\[
\operatorname{ARE}_P[\chi^*]\leq\min_{e\in\mathcal A(P)}\left\{\frac{\mathcal I(P,\mathcal H_0)}{\mathcal I(P^e,\mathcal H^e)}\right\}.
\]
Moreover, $\operatorname{ARE}_P[\chi^*]=1$ when there is exactly one dependent pair that is independent of all other data sources under $P$, for example, when (23) holds and $|\mathcal A(P)|=1$.''',r'''Suppose that $\emptyset\in\Psi$, $P\in\mathcal H_0$, and $\alpha,\beta\to0$ while $\gamma$ and $\delta$ are either fixed or go to $0$. If $s_e=e$ for every $e\in\mathcal K$ then
\[
\operatorname{ARE}_P[\chi^*]\leq\frac{\min_{e\in\mathcal K}\mathcal I(P,\mathcal G_{\Psi,e})}{\min_{e\in\mathcal K}\mathcal I(P^e,\mathcal G^e)}.
\]
If, also, $\Psi_{1,1}\subseteq\Psi$, and there is a pair of data sources that is independent of all other data sources under $P$ and achieves $\min_{e\in\mathcal K}\mathcal I(P^e,\mathcal G^e)$, e.g., when (23) holds, then $\operatorname{ARE}_P[\chi^*]=1$.''',r'''Suppose that $\Psi=\Psi_{\mathrm{dis}}$, $P\in\mathcal P_\Psi$ and $s_e=s'_e=e$ for every $e\in\mathcal K$. If (23) holds, and there is a pair of data sources that is independent of all other data sources under $P$ and achieves $\min_{e\notin\mathcal A(P)}\mathcal I(P^e,\mathcal G^e)$, then $\chi^*_{\mathrm{fwer}}$ is asymptotically optimal as $\gamma,\delta\to0$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; full original statement, including continuation where present') for p in pages]) for i,(n,s,pages) in enumerate(zip(NUMBERS,STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Joint sequential detection and isolation for dependent data streams',authors=['Anamitra Chaudhuri','Georgios Fellouris'],version='arXiv:2207.00120v1; arXiv stamp 30 Jun 2022',pdf_pages=80,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=25,main_text_boundary=dict(location='Main text ends with Section 8 Conclusion and the Funding statement on PDF page 25. Appendix A starts on a new PDF page 26. All appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerated actual small-cap THEOREM environments across PDF pages 1–25 and visually compared all twenty complete bodies. Theorems 5.2 and 6.2 continue on the next page. Excluded citations, proof headings, Corollaries, examples and appendices.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v1; no replacement source, web search or appendix-body reading.',normalization_policy='Original statement wording, formulas, subparts, branch quantifiers and irregularities retained; PDF wrapping and mathematical typesetting normalized only. Standing assumptions remain separate from the original theorem bodies.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved twenty complete original main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
