'use client';

import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';

export default function SubscribeButton() {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      const res = await fetch('/v1/stripe/session', { method: 'POST' });
      if (!res.ok) throw new Error('Failed to create session');
      const data = await res.json();
      const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY ?? '');
      if (!stripe) throw new Error('Stripe failed to load');
      const { error } = await stripe.redirectToCheckout({ sessionId: data.sessionId });
      if (error) {
        // eslint-disable-next-line no-console
        console.error(error);
      }
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={loading}
      className="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-50"
    >
      {loading ? 'Loading...' : 'Subscribe'}
    </button>
  );
}
